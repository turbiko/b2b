from datetime import datetime, date

from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from django.contrib.auth.models import User
from django.core.mail import send_mail, send_mass_mail

from project.models import Projects, \
	Project, \
	FileFolder, \
	FileInFolder, \
	NewsArticle, \
	FilesToFolder, \
	Photo, \
	select_last_topics

class Command(BaseCommand):
	help = 'Send email changes for few days in project'

	def handle(self, *args, **options):
		print('email will be send')
		# get projects
		all_pages = Projects.objects.all().live()
		i = 0
		text = []
		for child_page in all_pages:
			print(child_page.title)
			print('len text: ', len(text))
			text.append(select_last_topics(child_page))
			print(text)
			if i < (len(text)-1):
				i += 1
			else:
				print('end of cycle')
		## get active users list with email
		### in each project get groupname for searching users
		#### set period for report
		#### get changed pages in project title+url
		#### 1. from django.utils import timesince
		# timesince.timesince(self.date_posted)
		# {{ post.last_published_at|date:"F d, Y" }}
		# {{ post.last_published_at|timesince }}
		# {{ blog_date|timesince }}
		##### for each user send list of changed pages
		n = 0
		message = []
		print('-Len text', len(text))
		for t in text:
			print(n)
			message_tmp = (
			f'B2B updates digest {datetime.now()}', text[n].replace(u'\xa0', u' '), 'noreply@argentum.ua', ['a.voznyuk@film.ua',])
			if n < (len(text) - 1):
				n += 1
			else:
				print('end of cycle')
			message.append(message_tmp)
		print("Start messaging: ")
		messages = (message_text for message_text in message)
		print('messages: ', messages)
		send_mass_mail(messages, fail_silently=False)

		print('----===----')
		for admin_name, email in settings.ADMINS:
			if False:
				try:
					self.stdout.write(self.style.WARNING("About to send email to %s" % (email)))
					# Logic to send email here
					send_mail(
							'Subject b2b',
							'Here is the b2b message.',
							'noreply@argentum.ua',
							['a.voznyuk@film.ua'],
							fail_silently=False,
					)
					print('email sent: ', email)
					# Any other Python logic can also go here
					self.stdout.write(self.style.SUCCESS('Successfully sent email to "%s"' % email))
					# raise Exception
				except Exception:
					print('email not sent: ', email)
					raise CommandError('Failed to send test email')