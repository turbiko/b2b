from datetime import datetime, date, timedelta

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User, Group
from django.core.mail import send_mail, send_mass_mail
from django.utils.timesince import timesince
from django.core.mail import EmailMessage

from wagtail.models import Page, Orderable

from home.models import HomePage
from project.models import Projects, \
	Project, \
	FileFolder, \
	FileInFolder, \
	NewsArticle, \
	FilesToFolder, \
	Photo

DAYS_FOR_SENDCHANGES = 7

class Command(BaseCommand):
	help = 'Send email changes for few days in project'

	def handle(self, *args, **options):
		self.stdout.write(self.style.WARNING("email will be send"))
		# get groups, that not default and create list
		prj_groups = []
		for group1 in Group.objects.all():  # getting all projects groups to list
			if group1.name not in ('Moderators', 'Editors'):
				prj_groups.append(group1.name)
		# DEBUG, INFO, WARNING, ERROR, CRITICAL
		self.stdout.write(self.style.WARNING(prj_groups))

		## get projects for mailing
		active_projects = Page.objects.exact_type(Project).live()
		mail_content = {}
		# mail_to = {}
		for project in active_projects:
			mail_content[project.slug] = self.select_last_topics(project)
			self.stdout.write(self.style.WARNING(f'mail_content:{project.slug=} _ {mail_content[project.slug]}'))
			emails = self.get_subscriber_emails(project)
			if emails and mail_content[project.slug]:
				try:
					self.stdout.write(self.style.WARNING(f"About to send email to {emails}"))
					# Logic to send email here
					for email_to_send in emails:
						send_mail(
								f'B2B [{project.title}] updates digest {datetime.now().date().strftime("%d %B, %Y")}',
								mail_content[project.slug].replace(u'\xa0', u' '),
								settings.EMAIL_HOST_USER,
								[email_to_send],
								fail_silently=False,
						)
					self.stdout.write(self.style.WARNING("After successful sent email "))
				except Exception as ex:
					raise CommandError(f'Failed to send email to {emails=} \n {ex}')


	def select_last_topics(self, project_page, days=DAYS_FOR_SENDCHANGES) -> str:
		"""
		:param project_page: root page of project
		:param days: diapason for select pages
		:return: text content for  digest email  for period in days
		"""
		pages = project_page.get_descendants()
		content = ''
		d0 = date.today()
		d1 = d0 - timedelta(days=days)
		self.stdout.write(self.style.WARNING(f'today: {d1}  time-delta: {d0} _ days: {days}'))

		pages_for_report = pages.filter(last_published_at__gte=d1)
		for p in pages_for_report:
			# print(p.last_published_at.date(), d0, d1)
			content += str(timesince(p.last_published_at).split(',')[0]).replace(u'\xa0', u' ')
			content += f' {p.title}  {p.url}  \n '
		if content == '':
			self.stdout.write(self.style.WARNING(f'no changes since {str(d1)}'))

		self.stdout.write(self.style.WARNING(f'content({project_page.title}): {content}'))
		return content


	def get_subscriber_emails(self, project_page:Project) -> list:
		self.stdout.write(self.style.WARNING(f'Create emails list for {project_page.title=}'))
		try:
			selected_group = Group.objects.get(name=project_page.slug)
		except Group.DoesNotExist:
			self.stdout.write(self.style.WARNING(f'Group does not exist. Creating new group {project_page.slug} '))
			selected_group = Group.objects.create(name=project_page.slug)
		project_users = selected_group.user_set.all()  # users in group
		emails_to_send = []
		if project_users:
			for u in project_users:
				emails_to_send.append(u.email)
			self.stdout.write(self.style.WARNING(f'Created emails list for {project_page.title=}'))
		else:
			self.stdout.write(self.style.WARNING(f'No users in the group {project_page.slug}. Skip creating users list.'))
		return emails_to_send
