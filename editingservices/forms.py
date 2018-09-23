from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import User
from . models import *
from django.conf import settings
from datetime import datetime

from dal import autocomplete


class LoginForm(forms.Form):
     username = forms.CharField(widget=forms.TextInput(attrs={
         'class': 'input100',
         'placeholder': 'Email',
     }), error_messages={'required': 'Please enter username !'}, label="Username ", label_suffix="")
     password = forms.CharField(widget=forms.PasswordInput(attrs={
         'class': 'input100',
         'placeholder': 'Password',
     }), error_messages={'required': 'Please enter  password !'}, label="Password", label_suffix="")

class ArticleForm(forms.ModelForm):
	CHOICES_AOUTHO_TYPE = (('','Select One'),('Partner','Partner'),('Researcher','Researcher'),)
	catagory = forms.ChoiceField(choices=CHOICES_AOUTHO_TYPE, required=True, label='Catagory',label_suffix="",)
	article_title = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'Article title'}), label="Article title", label_suffix="", error_messages={'required':'Article title is requred !' })
	subject_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'Subject name'}), label="Subject name", label_suffix="", required = False)
	word_count = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'Word count'}), label="Word count", label_suffix="", required = False)
	paper_received = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'Paper received date'}), label="Paper received date", label_suffix="", required = False)
	expected_delivery_date = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'Expected delivery date'}), label="Expected delivery date", label_suffix="", required = False)
	class Meta:
		model = Article
		fields = ['catagory','article_title','subject_name','word_count','paper_received','expected_delivery_date']

class ArticleeditForm(forms.ModelForm):
	CHOICES_AOUTHO_TYPE = (('','Select One'),('Partner','Partner'),('Researcher','Researcher'),)
	catagory = forms.ChoiceField(choices=CHOICES_AOUTHO_TYPE, required=True, label='Catagory',label_suffix="",)
	article_title = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'Article title'}), label="Article title", label_suffix="", error_messages={'required':'Article title is requred !' })
	class Meta:
		model = Article
		fields = ['catagory','article_title']

class SubjectwordForm(forms.ModelForm):
	subject_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'Subject name'}), label="Subject name", label_suffix="", required = False)
	word_count = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'Word count'}), label="Word count", label_suffix="", required = False)
	class Meta:
		model=Article
		fields=['subject_name','word_count',]


class StageForm(forms.ModelForm):
	paper_received = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'Paper received date'}), label="Paper received date", label_suffix="", required = False)
	expected_delivery_date = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'Expected delivery date'}), label="Expected delivery date", label_suffix="", required = False)
	class Meta:
		model = Article
		fields = ['paper_received','expected_delivery_date']
		
class PaymentcertificateForm(forms.ModelForm):
	paper_sent_author = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'Paper sent author'}), label="Paper sent author", label_suffix="", required = False)
	payment_received_on = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'Payment received on'}), label="Payment received on", label_suffix="", required = False)
	
	class Meta:
		model = Article
		fields = ['paper_sent_author','payment_received_on']

class PdfeditForm(forms.ModelForm):
	class Meta:
		model = Article
		fields = ['pdf_authors_edit','pdf_issue_date_edit']			

class ArticlePartnerForm(forms.ModelForm):
	partner = forms.ModelChoiceField(label="Partner", queryset=Partner.objects.all() ,widget=forms.Select(attrs={'class':'form-control'}), required = False,  label_suffix="")
	partner_serial_send_no = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'Partner serial send no'}), label="Partner serial send no", label_suffix="", required = False)
	class Meta:
		model = ArticlePartner
		fields = ['partner','partner_serial_send_no']

class ArticleEditorForm(forms.ModelForm):
	CHOICES_SERVICE_TYPE = (('','Select one'),('GBP','GBP(£)'),('AUD','AUD(A$)'),('Euro','Euro(€)'),('USD','USD($)'),)
	EN_ED_OPTIONS = (('','----',),('English editing','English editing'))
	SC_ED_OPTIONS = (('','----',),('Scientific editing','Scientific editing'))
	PR_SUB_OPTIONS = (('','----',),('Presubmission review','Presubmission review'))
	JO_SE_OPTIONS = (('','----',),('Journal selection','Journal selection'))
	service_currency = forms.ChoiceField(choices=CHOICES_SERVICE_TYPE, required=True, label='Service currency',label_suffix="",)
	english_editing = forms.ChoiceField( choices=EN_ED_OPTIONS, required=False, label='English editing',label_suffix="", widget=forms.Select(attrs={'class':'form-control'}))
	english_editing_price = forms.FloatField(widget=forms.NumberInput(attrs={'class': 'form-control'}), label="Serevice amount", label_suffix="", required = False, initial=0.0)
	scientific_editing = forms.ChoiceField( choices=SC_ED_OPTIONS, required=False, label='Scientific editing',label_suffix="", widget=forms.Select(attrs={'class':'form-control'}))
	scientific_editing_price = forms.FloatField(widget=forms.NumberInput(attrs={'class': 'form-control'}), label="Serevice amount", label_suffix="", required = False, initial=0.0)
	presubmission_review = forms.ChoiceField( choices=PR_SUB_OPTIONS, required=False, label='Presubmission review',label_suffix="", widget=forms.Select(attrs={'class':'form-control'}))
	presubmission_review_price = forms.FloatField(widget=forms.NumberInput(attrs={'class': 'form-control'}), label="Serevice amount", label_suffix="", required = False, initial=0.0)
	journal_selection = forms.ChoiceField( choices=JO_SE_OPTIONS, required=False, label='Journal selection',label_suffix="", widget=forms.Select(attrs={'class':'form-control'}))
	journal_selection_price = forms.FloatField(widget=forms.NumberInput(attrs={'class': 'form-control'}), label="Serevice amount", label_suffix="", required = False, initial=0.0)
	paper_sent_editor = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'Paper sent editor'}), label="Paper sent editor", label_suffix="", required = False)
	expected_returned_paper = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'Expected returned paper'}), label="Expected returned paper", label_suffix="", required = False)
	editor_returned_paper = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'Editor returned paper'}), label="Editor returned paper", label_suffix="", required = False)
	editor_invoice_no = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'Editor invoice no'}), label="Editor invoice no", label_suffix="", required = False)
	editor_payment_sent = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'Editor payment sent'}), label="Editor payment sent", label_suffix="", required = False)
	class Meta:
		model = ArticleEditor
		fields = ['editor','service_currency','english_editing','english_editing_price','scientific_editing','scientific_editing_price','presubmission_review','presubmission_review_price','journal_selection','journal_selection_price','paper_sent_editor','expected_returned_paper','editor_returned_paper','editor_invoice_no','editor_payment_sent']


class PartnerForm(forms.ModelForm):
	partner_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'Partner name'}), label="Partner name", label_suffix="", error_messages={'required':'Partner name is requred !' })
	partner_contact = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'Partner contact'}), label="Partner contact", label_suffix="", required = False)
	partner_address = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'Partner address'}), label="Partner address", label_suffix="", required = False)
	partner_partner_country = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'Partner country'}), label="Partner country", label_suffix="", required = False)
	partner_email = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'E-mail'}), label="E-mail", label_suffix="", required = False)
	partner_tel = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'Partner tel'}), label="Partner tel", label_suffix="", required = False)
	partner_note = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'Partner note'}), label="Partner note", label_suffix="", required = False)
	class Meta:
		model = Partner
		fields = ['partner_name','partner_contact','partner_address','partner_partner_country','partner_email','partner_tel','partner_note']


class AuthorForm(forms.ModelForm):
	CHOICES_AOUTHO_TYPE = (('','Select One'),('Author','Author'),('Co-author','Co-author'),)
	author_type = forms.ChoiceField(choices=CHOICES_AOUTHO_TYPE, required=True, label='Catagory',label_suffix="",)
	author_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'Author name'}), label="Author name", label_suffix="", error_messages={'required':'Author name is requred !' })
	affiliation = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'Affiliation'}), label="Affiliation", label_suffix="", required = False)
	department = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'Department'}), label="Department", label_suffix="", required = False)
	address = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'Address'}), label="Address", label_suffix="", required = False)
	author_country = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'Authorn  country'}), label="Author country", label_suffix="", required = False)
	email = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'E-mail'}), label="E-mail", label_suffix="", required = False)
	tel = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'tel'}), label="Tel", label_suffix="", required = False)
	orcid_id = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'Orcid iD'}), label="Orcid iD", label_suffix="", required = False)
	class Meta:
		model = Author
		fields = ['author_type','author_name','affiliation','department','address','author_country','email','tel','orcid_id']


class TargetjournalForm(forms.ModelForm):
	journal_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'Journal name'}), label="Journal name", label_suffix="", error_messages={'required':'Journal name is requred !' })
	publisher_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'Publisher name'}), label="Publisher name", label_suffix="", required = False)
	issn = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'issn'}), label="ISSN", label_suffix="", required = False)
	impact_factor = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'Impact factor'}), label="Impact factor", label_suffix="", required = False)

	class Meta:
		model = Target_journal
		fields = ['journal_name','publisher_name','issn','impact_factor']

class ServiceForm(forms.ModelForm):
	CHOICES_SERVICE_TYPE = (('','Select one'),('GBP','GBP(£)'),('AUD','AUD(A$)'),('Euro','Euro(€)'),('USD','USD($)'),)
	EN_ED_OPTIONS = (('','----',),('English editing','English editing'))
	SC_ED_OPTIONS = (('','----',),('Scientific editing','Scientific editing'))
	PR_SUB_OPTIONS = (('','----',),('Presubmission review','Presubmission review'))
	JO_SE_OPTIONS = (('','----',),('Journal selection','Journal selection'))
	service_currency = forms.ChoiceField(choices=CHOICES_SERVICE_TYPE, required=True, label='Service currency',label_suffix="",)
	english_editing = forms.ChoiceField( choices=EN_ED_OPTIONS, required=False, label='English editing',label_suffix="", widget=forms.Select(attrs={'class':'form-control'}))
	english_editing_price = forms.FloatField(widget=forms.NumberInput(attrs={'class': 'form-control'}), label="Serevice amount", label_suffix="", required = False, initial=0.0)
	scientific_editing = forms.ChoiceField( choices=SC_ED_OPTIONS, required=False, label='Scientific editing',label_suffix="", widget=forms.Select(attrs={'class':'form-control'}))
	scientific_editing_price = forms.FloatField(widget=forms.NumberInput(attrs={'class': 'form-control'}), label="Serevice amount", label_suffix="", required = False, initial=0.0)
	presubmission_review = forms.ChoiceField( choices=PR_SUB_OPTIONS, required=False, label='Presubmission review',label_suffix="", widget=forms.Select(attrs={'class':'form-control'}))
	presubmission_review_price = forms.FloatField(widget=forms.NumberInput(attrs={'class': 'form-control'}), label="Serevice amount", label_suffix="", required = False, initial=0.0)
	journal_selection = forms.ChoiceField( choices=JO_SE_OPTIONS, required=False, label='Journal selection',label_suffix="", widget=forms.Select(attrs={'class':'form-control'}))
	journal_selection_price = forms.FloatField(widget=forms.NumberInput(attrs={'class': 'form-control'}), label="Serevice amount", label_suffix="", required = False, initial=0.0)
	author_invoice_number = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), label="Invoice number", label_suffix="", required = False)
	date_invoice = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'Invoice date'}), label="Invoice date", label_suffix="", required = False)
	
	class Meta:
		model = Service
		fields = ['service_currency','english_editing','english_editing_price','scientific_editing','scientific_editing_price','presubmission_review','presubmission_review_price','journal_selection','journal_selection_price','author_invoice_number','date_invoice']

class EditorForm(forms.ModelForm):
	editor_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'Editor name'}), label="Editor name", label_suffix="", error_messages={'required':'Editor name is requred !' })
	education = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'Education'}), label="Education", label_suffix="", required = False)
	subject_covers = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'Subject covers'}), label="Subject covers", label_suffix="", required = False)
	address = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'Address'}), label="Address", label_suffix="", required = False)
	editor_country = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'Editor country'}), label="Editor country", label_suffix="", required = False)
	email = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'E-mail'}), label="E-mail", label_suffix="", required = False)
	tel = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'Tel'}), label="Tel", label_suffix="", required = False)
	rate = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'Rate'}), label="Rate", label_suffix="", required = False)
	editor_note = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'Editor note'}), label="Editor note", label_suffix="", required = False)

	class Meta:
		model = Editor
		fields = ['editor_name','education','subject_covers','address','editor_country','email','tel','rate','editor_note']




