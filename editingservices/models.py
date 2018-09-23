from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from django.utils.text import slugify

from django.core.validators import URLValidator
import datetime
from django.conf import settings
from editingapp import utils

def create_id():
	last_booking = Article.objects.all().order_by('id').last()
	if not last_booking:
		return 'ESI-' + str(datetime.date.today().year) + str(datetime.date.today().month).zfill(2) + '-' + '0000000001'
	booking_id = last_booking.booking_id
	booking_int = int(booking_id[13:21])
	new_booking_int = booking_int + 1
	new_booking_id = 'ESI-' + str(str(datetime.date.today().year)) + str(datetime.date.today().month).zfill(2) + '-' + str(new_booking_int).zfill(10)
	return new_booking_id

class Partner(models.Model):
	partner_name = models.CharField(max_length=150)
	partner_contact = models.CharField(max_length=150)
	partner_address = models.CharField(max_length=250)
	partner_partner_country = models.CharField(max_length=50)
	partner_email = models.CharField(max_length=150)
	partner_tel = models.CharField(max_length=150)
	partner_note = models.CharField(max_length=1000)

	def __str__(self):
		return self.partner_name

class Editor(models.Model):
	editor_name = models.CharField(max_length=150, null=True, blank=True)
	education = models.CharField(max_length=150)
	subject_covers = models.CharField(max_length=1000,null=True, blank=True)
	address = models.CharField(max_length=250)
	editor_country = models.CharField(max_length=50)
	email = models.CharField(max_length=150)
	tel = models.CharField(max_length=150)
	rate = models.CharField(max_length=50)
	editor_note = models.CharField(max_length=1000)

	def __str__(self):
		return self.editor_name

class Article(models.Model):
	ARTICLE_TYPE = (
		('','Select One'),
		('Partner','Partner'),
		('Researcher','Researcher'),
	)
	catagory = models.CharField(max_length=20, choices=ARTICLE_TYPE)
	article_title = models.CharField(max_length=250)
	subject_name = models.CharField(max_length=150,null=True, blank=True)
	word_count = models.CharField(max_length=150,null=True, blank=True)
	paper_received = models.CharField(max_length=10,null=True, blank=True)
	expected_delivery_date = models.CharField(max_length=10, null=True, blank=True)
	paper_sent_author = models.CharField(max_length=10, null=True, blank=True)
	payment_received_on = models.CharField(max_length=10, null=True, blank = True)
	booking_id = models.CharField(max_length=250, default=create_id, editable=False)
	slug = models.SlugField(max_length=120, blank=True, unique=True)

	#for edit pdf field
	pdf_authors_edit = models.CharField(max_length=1000, null=True, blank = True)
	pdf_issue_date_edit = models.CharField(max_length=1000, null=True, blank = True)
	def get_absolute_url(self):
		return reverse('article_detail', kwargs={"slug": self.slug})
	def _get_unique_slug(self):
		slug = slugify(self.article_title)
		unique_slug = slug
		num = 1
		while Article.objects.filter(slug=unique_slug).exists():
			unique_slug = '{}-{}'.format(slug, num)
			num += 1
		return unique_slug
	def save(self, *args, **kwargs):
		if not self.pk:
			self.slug = self._get_unique_slug()
		super(Article, self).save(*args, **kwargs)
	def __str__(self):
		return self.article_title

class ArticlePartner(models.Model):
	article = models.ForeignKey(Article, on_delete = models.CASCADE)
	partner = models.ForeignKey(Partner, on_delete = models.CASCADE, null=True, blank=True)
	partner_serial_send_no = models.CharField(max_length=250, null=True, blank=True)
	def __str__(self):
		return self.editor

class ArticleEditor(models.Model):
	CURRENCY_OPTIONS = (
		('GBP','GBP(£)'),
		('AUD','AUD(A$)'),
		('Euro','Euro(€)'),
		('USD','USD($)'),
	)
	EN_ED_OPTIONS = (
		('','----',),
		('English editing','English editing')
	)
	SC_ED_OPTIONS = (
		('','----',),
		('Scientific editing','Scientific editing'),
	)
	PR_SUB_OPTIONS = (
		('','----',),
		('Presubmission review','Presubmission review'),
	)
	JO_SE_OPTIONS = (
		('','----',),
		('Journal selection','Journal selection'),
	)
	
	article = models.ForeignKey(Article, on_delete = models.CASCADE)
	editor = models.ForeignKey(Editor, on_delete = models.CASCADE)
	service_currency = models.CharField(max_length=20, choices=CURRENCY_OPTIONS)
	english_editing =  models.CharField(max_length=20,null=True, blank=True, choices=EN_ED_OPTIONS)
	english_editing_price = models.FloatField(null=True, blank=True, default=0.0)
	scientific_editing = models.CharField(max_length=20,null=True, blank=True, choices=SC_ED_OPTIONS)
	scientific_editing_price = models.FloatField(null=True, blank=True, default=0.0)
	presubmission_review = models.CharField(max_length=20,null=True, blank=True, choices=PR_SUB_OPTIONS)
	presubmission_review_price = models.FloatField(null=True, blank=True, default=0.0)
	journal_selection = models.CharField(max_length=20,null=True, blank=True, choices=JO_SE_OPTIONS)
	journal_selection_price = models.FloatField(null=True, blank=True, default=0.0)
	paper_sent_editor = models.CharField(max_length=10, null=True, blank=True)
	expected_returned_paper = models.CharField(max_length=10, null=True, blank=True)
	editor_returned_paper = models.CharField(max_length=10, null=True, blank=True)
	editor_invoice_no = models.CharField(max_length=1000, null= True, blank = True)
	editor_payment_sent = models.CharField(max_length=10, null=True, blank=True)
	def __str__(self):
		return str(self.id)
		
class Author(models.Model):
	AUTHOR_TYPE = (
		('','Select One'),
		('Author','Author'),
		('Co-author','Co-author'),
	)
	article = models.ForeignKey(Article, on_delete = models.CASCADE, null=True, blank=True)
	author_type = models.CharField(max_length=20, choices=AUTHOR_TYPE)
	author_name = models.CharField(max_length=150, null=True, blank=True)
	affiliation = models.CharField(max_length=150)
	department = models.CharField(max_length=150)
	address = models.CharField(max_length=250)
	author_country = models.CharField(max_length=50)
	email = models.CharField(max_length=150)
	tel = models.CharField(max_length=150)
	orcid_id = models.CharField(max_length=350)
	
	def __str__(self):
		return self.author_name



class Target_journal(models.Model):
	article = models.ForeignKey(Article, on_delete = models.CASCADE, null=True, blank=True)
	journal_name = models.CharField(max_length=150)
	publisher_name = models.CharField(max_length=150)
	issn = models.CharField(max_length=150)
	impact_factor = models.CharField(max_length=150)

	def __str__(self):
		return self.journal_name


class Service(models.Model):
	CURRENCY_OPTIONS = (
		('GBP','GBP(£)'),
		('AUD','AUD(A$)'),
		('Euro','Euro(€)'),
		('USD','USD($)'),
	)
	EN_ED_OPTIONS = (
		('','----',),
		('English editing','English editing')
	)
	SC_ED_OPTIONS = (
		('','----',),
		('Scientific editing','Scientific editing'),
	)
	PR_SUB_OPTIONS = (
		('','----',),
		('Presubmission review','Presubmission review'),
	)
	JO_SE_OPTIONS = (
		('','----',),
		('Journal selection','Journal selection'),
	)
	article = models.ForeignKey(Article, on_delete = models.CASCADE, null=True, blank=True)
	service_currency = models.CharField(max_length=20, choices=CURRENCY_OPTIONS)
	english_editing =  models.CharField(max_length=20,null=True, blank=True, choices=EN_ED_OPTIONS)
	english_editing_price = models.FloatField(null=True, blank=True, default=0.0)
	scientific_editing = models.CharField(max_length=20,null=True, blank=True, choices=SC_ED_OPTIONS)
	scientific_editing_price = models.FloatField(null=True, blank=True, default=0.0)
	presubmission_review = models.CharField(max_length=20,null=True, blank=True, choices=PR_SUB_OPTIONS)
	presubmission_review_price = models.FloatField(null=True, blank=True, default=0.0)
	journal_selection = models.CharField(max_length=20,null=True, blank=True, choices=JO_SE_OPTIONS)
	journal_selection_price = models.FloatField(null=True, blank=True, default=0.0)
	author_invoice_number = models.CharField(max_length=15, null=True, blank = True)
	date_invoice = models.CharField(max_length=10, null=True, blank = True)
	#payment_received_on = models.CharField(max_length=10, null=True, blank = True)


	def __str__(self):
		return self.service_currency

