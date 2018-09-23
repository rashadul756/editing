from django.shortcuts import render, redirect, render_to_response,get_object_or_404
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash, authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError

from django.views import generic
from django.db.models import Count, Sum

from django.template import RequestContext

from . forms import *
from .models import *

from datetime import datetime
from editingapp.utils import TimeStampModel 


from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.views.generic import View
from .utils import render_to_pdf 


def cleanhtml(raw_html):
  cleanr = re.compile('<.*?>')
  cleantext = re.sub(cleanr, '', raw_html)
  return cleantext


@method_decorator(login_required, name='dispatch')
class GeneratePDF(View):
	def get(self, request, slug, *args, **kwargs):
		
		
		template = get_template('pdf/certificate_pdf.htm')
		article = get_object_or_404(Article, slug=slug)
		context = {
			'article': article,
			'time':datetime.now(),
			}
		html = template.render(context)
		pdf = render_to_pdf('pdf/certificate_pdf.htm', context)
		if pdf:
			response = HttpResponse(pdf, content_type='application/pdf')
			filename = article.booking_id+".pdf" 
			content = "inline; filename='%s'" %(filename)
			download = request.GET.get("download")
			if download:
				content = "attachment; filename='%s'" %(filename)
			response['Content-Disposition'] = content
			return response
		return HttpResponse("Not found")

def index(request):
	form = LoginForm(request.POST or None)
	if form.is_valid():
		username = form.cleaned_data["username"]
		password = form.cleaned_data["password"]
		user = authenticate(username=username, password=password)
		if user is not None:
			login(request, user)
			#return render(request,"")
			return redirect('root_admin')
		else:
			error = "Username & Password didn't match !"
			form.add_error(None, error)
	context = {
		'title': 'Login',
		'form': form
	}
	return render(request, 'login.html', context)

@method_decorator(login_required, name='dispatch')
class ArticleView(generic.ListView):
	template_name = 'article.html'
	context_object_name = 'article'

	def get_context_data(self, **kwargs):
		# Call the base implementation first to get a context
		context = super(ArticleView, self).get_context_data(**kwargs)

		category_list = Article.objects.distinct().annotate(total_amount_earned=Count('article_title'))

		categories = {}
		letters = []
		for category in category_list:

			if category.catagory in categories:
				count = categories[category.catagory][0]
				new_count = count+1
				categories[category.catagory][0] = new_count
			else:
				categories[category.catagory] = [1,category.catagory]
			letters.append(category.article_title[0])
		count = {}
		context["letters"] = set(letters)
		context['category_list'] = categories 
		context['count_list'] = count
		context['total_article'] = len(category_list)

		return context

	def get_queryset(self):
		cat = self.kwargs.get("cat",None)
		charsort = self.kwargs.get("charsort",None)
		search = self.request.GET.get('search')


		query_set = None
		if cat is not None:
			query_set=Article.objects.filter(catagory=cat).order_by('-id')
		elif charsort is not None:
			query_set=Article.objects.filter(article_title__istartswith=charsort).order_by('-id')
		elif search is not None:
			query_set=Article.objects.filter(article_title__istartswith=search)
		else:
			query_set=Article.objects.all().order_by('-id')
		return query_set

@method_decorator(login_required, name='dispatch')
class ArticleprocesingstageView(generic.ListView):
	template_name = 'article_procesing_stage.html'
	context_object_name = 'article'

	def get_context_data(self, **kwargs):
		# Call the base implementation first to get a context
		context = super(ArticleprocesingstageView, self).get_context_data(**kwargs)

		category_list = Article.objects.distinct().annotate(total_amount_earned=Count('article_title'))

		categories = {}
		letters = []
		for category in category_list:

			if category.catagory in categories:
				count = categories[category.catagory][0]
				new_count = count+1
				categories[category.catagory][0] = new_count
			else:
				categories[category.catagory] = [1,category.catagory]
			letters.append(category.article_title[0])
		count = {}
		context["letters"] = set(letters)
		context['category_list'] = categories 
		context['count_list'] = count
		context['total_article'] = len(category_list)

		return context

	def get_queryset(self):
		cat = self.kwargs.get("cat",None)
		charsort = self.kwargs.get("charsort",None)
		search = self.request.GET.get('search')


		query_set = None
		if cat is not None:
			query_set=Article.objects.filter(catagory=cat).order_by('-id')
		elif charsort is not None:
			query_set=Article.objects.filter(article_title__istartswith=charsort).order_by('-id')
		elif search is not None:
			query_set=Article.objects.filter(article_title__istartswith=search)
		else:
			query_set=Article.objects.all().order_by('-id')
		return query_set

@method_decorator(login_required, name='dispatch')		
class ArticlesentauthorView(generic.ListView):
	template_name = 'article_sent_to_author.html'
	context_object_name = 'article'

	def get_context_data(self, **kwargs):
		# Call the base implementation first to get a context
		context = super(ArticlesentauthorView, self).get_context_data(**kwargs)

		category_list = Article.objects.distinct().annotate(total_amount_earned=Count('article_title'))

		categories = {}
		letters = []
		for category in category_list:

			if category.catagory in categories:
				count = categories[category.catagory][0]
				new_count = count+1
				categories[category.catagory][0] = new_count
			else:
				categories[category.catagory] = [1,category.catagory]
			letters.append(category.article_title[0])
		count = {}
		context["letters"] = set(letters)
		context['category_list'] = categories 
		context['count_list'] = count
		context['total_article'] = len(category_list)

		return context

	def get_queryset(self):
		cat = self.kwargs.get("cat",None)
		charsort = self.kwargs.get("charsort",None)
		search = self.request.GET.get('search')


		query_set = None
		if cat is not None:
			query_set=Article.objects.filter(catagory=cat).order_by('-id')
		elif charsort is not None:
			query_set=Article.objects.filter(article_title__istartswith=charsort).order_by('-id')
		elif search is not None:
			query_set=Article.objects.filter(article_title__istartswith=search)
		else:
			query_set=Article.objects.all().order_by('-id')
		return query_set

@method_decorator(login_required, name='dispatch')
class ArticlefinalstageView(generic.ListView):
	template_name = 'article_final_stage.html'
	context_object_name = 'article'

	def get_context_data(self, **kwargs):
		# Call the base implementation first to get a context
		context = super(ArticlefinalstageView, self).get_context_data(**kwargs)

		category_list = Article.objects.distinct().annotate(total_amount_earned=Count('article_title'))

		categories = {}
		letters = []
		for category in category_list:

			if category.catagory in categories:
				count = categories[category.catagory][0]
				new_count = count+1
				categories[category.catagory][0] = new_count
			else:
				categories[category.catagory] = [1,category.catagory]
			letters.append(category.article_title[0])
		count = {}
		context["letters"] = set(letters)
		context['category_list'] = categories 
		context['count_list'] = count
		context['total_article'] = len(category_list)

		return context

	def get_queryset(self):
		cat = self.kwargs.get("cat",None)
		charsort = self.kwargs.get("charsort",None)
		search = self.request.GET.get('search')


		query_set = None
		if cat is not None:
			query_set=Article.objects.filter(catagory=cat).order_by('-id')
		elif charsort is not None:
			query_set=Article.objects.filter(article_title__istartswith=charsort).order_by('-id')
		elif search is not None:
			query_set=Article.objects.filter(article_title__istartswith=search)
		else:
			query_set=Article.objects.all().order_by('-id')
		return query_set

@login_required	
def logout_view(request):
    logout(request)
    return redirect("/")

@login_required	
def root_admin(request):
	article = Article.objects.order_by('-id')
	context = {'article':article}
	return render(request, 'root_admin.html', context)

@login_required	
def create_article(request):
	
	if request.method=='POST':
		form = ArticleForm(request.POST or None)
		#partn1=request.POST['partner']
		#partner = Partner.objects.get(pk=partn1)
		if form.is_valid():
			new_article = Article(catagory=request.POST['catagory'],
				article_title=request.POST['article_title'],
				subject_name=request.POST['subject_name'],
				word_count=request.POST['word_count'],
				paper_received=request.POST['paper_received'],
				expected_delivery_date=request.POST['expected_delivery_date'])
			new_article.save()
			return redirect('root_admin')
	else:
		form = ArticleForm()

	template_name = 'form/create_article_form.html'
	context = {'form': form}
	return render(request, template_name, context)

@login_required	
def article_detail(request, slug):
	try:
		article=Article.objects.get(slug=slug)
	except Article.DoesNotExist:
		raise Http404("Article does not exist")

	return render(
        request,
        'article_detail.html',
        context={'article':article,}
    )

@login_required	
def article_edit_full(request, slug):
	article = Article.objects.get(slug=slug)
	if request.method=='POST':
		form = ArticleForm(request.POST, instance=article)
		if form.is_valid():
			form.save()
			return redirect('article_detail', slug=article.slug)
	else:
		form = ArticleForm(instance=article)

	template_name = 'form/edit_article_full_form.html'
	context = {'article': article,'form': form}
	return render(request, template_name, context)

@login_required	
def article_edit(request, slug):
	article = Article.objects.get(slug=slug)
	if request.method=='POST':
		form = ArticleeditForm(request.POST, instance=article)
		if form.is_valid():
			form.save()
			return redirect('article_detail', slug=article.slug)
	else:
		form = ArticleeditForm(instance=article)

	template_name = 'form/edit_article_form.html'
	context = {'article': article,'form': form}
	return render(request, template_name, context)

@login_required		
def article_delete(request, slug):
	article = Article.objects.get(slug=slug)
	if request.method=='POST':
		article.delete()
		return redirect('root_admin')
	template_name = 'form/delete_article_form.html'
	context = {'article': article}
	return render(request, template_name, context)

@login_required	
def article_pdf_editing(request, slug):
	a = Article.objects.get(slug=slug)
	if request.method=='POST':
		form = PdfeditForm(request.POST, instance=a)
		if form.is_valid():
			form.save()
			return redirect('article_pdf', slug=a.slug)
	else:
		form = PdfeditForm(instance=a)

	template_name = 'pdf/edit_pdf_form.html'
	context = {'a': a,'form': form}
	return render(request, template_name, context)

@login_required	
def subject_word_edit(request, slug):
	article = Article.objects.get(slug=slug)
	if request.method=='POST':
		form = SubjectwordForm(request.POST, instance=article)
		if form.is_valid():
			form.save()
			return redirect('article_detail', slug=article.slug)
	else:
		form = SubjectwordForm(instance=article)

	template_name = 'form/subject_word_edit_form.html'
	context = {'article': article,'form': form}
	return render(request, template_name, context)

@login_required	
def stage_add(request, slug):
	article = Article.objects.get(slug=slug)
	if request.method=='POST':
		form = StageForm(request.POST, instance=article)
		if form.is_valid():
			form.save()
			return redirect('article_detail', slug=article.slug)
	else:
		form = StageForm(instance=article)

	template_name = 'form/add_stage_form.html'
	context = {'article': article,'form': form}
	return render(request, template_name, context)

@login_required	
def payment_delivery_add(request, slug):
	article = Article.objects.get(slug=slug)
	if request.method=='POST':
		form = PaymentcertificateForm(request.POST, instance=article)
		if form.is_valid():
			form.save()
			return redirect('article_detail', slug=article.slug)
	else:
		form = PaymentcertificateForm(instance=article)

	template_name = 'form/add_payment_delivery_form.html'
	context = {'article': article,'form': form}
	return render(request, template_name, context)

@login_required	
def author_add(request, slug):
	article = Article.objects.get(slug=slug)
	if request.method=='POST':
		form = AuthorForm(request.POST)

		if form.is_valid():
			new_author = Author(author_type=request.POST['author_type'],
				author_name=request.POST['author_name'],
				affiliation=request.POST['affiliation'],
				department=request.POST['department'],
				address=request.POST['address'],
				author_country=request.POST['author_country'],
				email=request.POST['email'],
				tel=request.POST['tel'],
				orcid_id=request.POST['orcid_id'])
			new_author.article = article
			new_author.save()
			return redirect('article_detail', slug=article.slug)
	else:
		form = AuthorForm()

	template_name = 'form/create_author_form.html'
	context = {'article': article,'form': form}
	return render(request, template_name, context)

@login_required	
def author_edit(request, slug, pk):
	article = Article.objects.filter(slug=slug)
	author = Author.objects.get(pk=pk)
	if request.method=='POST':
		form = AuthorForm(request.POST, instance=author)
		if form.is_valid():
			form.save()
			return redirect('article_detail', slug=slug)
	else:
		form = AuthorForm(instance=author)

	template_name = 'form/edit_author_form.html'
	context = {'article': article,'author': author,'form': form}
	return render(request, template_name, context)

@login_required	
def author_delete(request, slug, pk):
	article = Article.objects.filter(slug=slug)
	author = Author.objects.get(pk=pk)
	if request.method=='POST':
		author.delete()
		return redirect('article_detail', slug=slug)
	template_name = 'form/delete_article_author_form.html'
	context = {'article': article,'author': author,}
	return render(request, template_name, context)

@login_required	
def target_journal_add(request, slug):
	article = Article.objects.get(slug=slug)
	if request.method=='POST':
		form = TargetjournalForm(request.POST)

		if form.is_valid():
			new_target_journal = Target_journal(journal_name=request.POST['journal_name'],
				publisher_name=request.POST['publisher_name'],
				issn=request.POST['issn'],
				impact_factor=request.POST['impact_factor'])
			new_target_journal.article = article
			new_target_journal.save()
			return redirect('article_detail', slug=article.slug)
	else:
		form = TargetjournalForm()

	template_name = 'form/create_target_journal_form.html'
	context = {'article': article,'form': form}
	return render(request, template_name, context)

@login_required	
def target_journal_edit(request, slug, pk):
	article = Article.objects.filter(slug=slug)
	target_journal = Target_journal.objects.get(pk=pk)
	if request.method=='POST':
		form = TargetjournalForm(request.POST, instance=target_journal)
		if form.is_valid():
			form.save()
			return redirect('article_detail', slug=slug)
	else:
		form = TargetjournalForm(instance=target_journal)

	template_name = 'form/edit_target_journal_form.html'
	context = {'article': article,'target_journal': target_journal,'form': form}
	return render(request, template_name, context)

@login_required	
def target_journal_delete(request, slug, pk):
	article = Article.objects.filter(slug=slug)
	target_journal = Target_journal.objects.get(pk=pk)
	if request.method=='POST':
		target_journal.delete()
		return redirect('article_detail', slug=slug)
	template_name = 'form/delete_article_target_journal_form.html'
	context = {'article': article,'target_journal': target_journal,}
	return render(request, template_name, context)

@login_required	
def service_add(request, slug):
	article = Article.objects.get(slug=slug)
	if request.method=='POST':
		form = ServiceForm(request.POST)

		if form.is_valid():
			new_service = Service(service_currency=request.POST['service_currency'],
				english_editing=request.POST['english_editing'],
				english_editing_price=request.POST['english_editing_price'],
				scientific_editing=request.POST['scientific_editing'],
				scientific_editing_price=request.POST['scientific_editing_price'],
				presubmission_review=request.POST['presubmission_review'],
				presubmission_review_price=request.POST['presubmission_review_price'],
				journal_selection=request.POST['journal_selection'],
				journal_selection_price=request.POST['journal_selection_price'],
				author_invoice_number=request.POST['author_invoice_number'],
				date_invoice=request.POST['date_invoice'])
			new_service.article = article
			new_service.save()
			return redirect('article_detail', slug=article.slug)
	else:
		form = ServiceForm()

	template_name = 'form/create_service_form.html'
	context = {'article': article,'form': form}
	return render(request, template_name, context)

@login_required	
def service_edit(request, slug, pk):
	article = Article.objects.filter(slug=slug)
	service = Service.objects.get(pk=pk)
	if request.method=='POST':
		form = ServiceForm(request.POST, instance=service)
		if form.is_valid():
			form.save()
			return redirect('article_detail', slug=slug)
	else:
		form = ServiceForm(instance=service)

	template_name = 'form/edit_author_invoice_form.html'
	context = {'article': article,'service': service,'form': form}
	return render(request, template_name, context)

@login_required	
def service_delete(request, slug, pk):
	article = Article.objects.filter(slug=slug)
	service = Service.objects.get(pk=pk)
	if request.method=='POST':
		service.delete()
		return redirect('article_detail', slug=slug)
	template_name = 'form/delete_author_invoice_form.html'
	context = {'article': article,'service': service,}
	return render(request, template_name, context)

@login_required	
def partner_add(request, slug):
	article = Article.objects.get(slug=slug)
	if request.method=='POST':
		form = ArticlePartnerForm(request.POST)
		partner1=request.POST['partner']
		partner = Partner.objects.get(pk=partner1)
		if form.is_valid():
			new_articlepartner = ArticlePartner(partner_serial_send_no=request.POST['partner_serial_send_no'])
			new_articlepartner.partner = partner
			new_articlepartner.article = article
			new_articlepartner.save()
			return redirect('article_detail', slug=article.slug)
	else:
		form = ArticlePartnerForm()

	template_name = 'form/add_article_partner_form.html'
	context = {'article': article,'form': form}
	return render(request, template_name, context)

@login_required	
def partner_article_edit(request, slug, pk):
	article = Article.objects.filter(slug=slug)
	articlepartner = ArticlePartner.objects.get(pk=pk)
	if request.method=='POST':
		form = ArticlePartnerForm(request.POST, instance=articlepartner)
		if form.is_valid():
			form.save()
			return redirect('article_detail', slug=slug)
	else:
		form = ArticlePartnerForm(instance=articlepartner)

	template_name = 'form/edit_article_partner_form.html'
	context = {'article': article,'articlepartner': articlepartner,'form': form}
	return render(request, template_name, context)

@login_required	
def partner_article_delete(request, slug, pk):
	article = Article.objects.filter(slug=slug)
	articlepartner = ArticlePartner.objects.get(pk=pk)
	if request.method=='POST':
		articlepartner.delete()
		return redirect('article_detail', slug=slug)
	template_name = 'form/delete_article_partner_form.html'
	context = {'article': article,'articlepartner': articlepartner,}
	return render(request, template_name, context)

@login_required	
def editor_add(request, slug):
	article = Article.objects.get(slug=slug)
	if request.method=='POST':
		form = ArticleEditorForm(request.POST)
		editor1=request.POST['editor']
		editor = Editor.objects.get(pk=editor1)
		if form.is_valid():
			new_articleeditor = ArticleEditor(service_currency = request.POST['service_currency'],
				english_editing = request.POST['english_editing'],
				english_editing_price = request.POST['english_editing_price'],
				scientific_editing = request.POST['scientific_editing'],
				scientific_editing_price = request.POST['scientific_editing_price'],
				presubmission_review = request.POST['presubmission_review'],
				presubmission_review_price = request.POST['presubmission_review_price'],
				journal_selection = request.POST['journal_selection'],
				journal_selection_price = request.POST['journal_selection_price'],
				paper_sent_editor = request.POST['paper_sent_editor'],
				expected_returned_paper = request.POST['expected_returned_paper'],
				editor_returned_paper = request.POST['editor_returned_paper'],
				editor_invoice_no = request.POST['editor_invoice_no'],
				editor_payment_sent = request.POST['editor_payment_sent'])
			new_articleeditor.editor = editor
			new_articleeditor.article = article
			new_articleeditor.save()
			return redirect('article_detail', slug=article.slug)
	else:
		form = ArticleEditorForm()

	template_name = 'form/add_article_editor_form.html'
	context = {'article': article,'form': form}
	return render(request, template_name, context)

@login_required	
def editor_edit(request, slug, pk):
	article = Article.objects.filter(slug=slug)
	articleeditor = ArticleEditor.objects.get(pk=pk)
	if request.method=='POST':
		form = ArticleEditorForm(request.POST, instance=articleeditor)
		if form.is_valid():
			form.save()
			return redirect('article_detail', slug=slug)
	else:
		form = ArticleEditorForm(instance=articleeditor)

	template_name = 'form/edit_article_editor_form.html'
	context = {'article': article,'articleeditor': articleeditor,'form': form}
	return render(request, template_name, context)

@login_required	
def editor_delete(request, slug, pk):
	article = Article.objects.filter(slug=slug)
	articleeditor = ArticleEditor.objects.get(pk=pk)
	if request.method=='POST':
		articleeditor.delete()
		return redirect('article_detail', slug=slug)
	template_name = 'form/delete_article_editor_form.html'
	context = {'article': article,'articleeditor': articleeditor,}
	return render(request, template_name, context)

@login_required	
def create_partner(request):
	if request.method=='POST':
		form = PartnerForm(request.POST)

		if form.is_valid():
			new_partner = Partner(partner_name=request.POST['partner_name'],
				partner_contact=request.POST['partner_contact'],
				partner_address=request.POST['partner_address'],
				partner_partner_country=request.POST['partner_partner_country'],
				partner_email=request.POST['partner_email'],
				partner_tel=request.POST['partner_tel'],
				partner_note=request.POST['partner_note'])
			new_partner.save()
			return redirect('partner_list')
	else:
		form = PartnerForm()

	template_name = 'form/create_partner_form.html'
	context = {'form': form}
	return render(request, template_name, context)

@login_required	
def edit_partner(request, id):
	partner = Partner.objects.get(pk=id)
	if request.method=='POST':
		form = PartnerForm(request.POST, instance=partner)
		if form.is_valid():
			form.save()
			return redirect('partner_list')
	else:
		form = PartnerForm(instance=partner)
	template_name = 'form/edit_partner_form.html'
	context = {'form': form}
	return render(request, template_name, context)

@login_required	
def delete_partner(request, id):
	partner = Partner.objects.get(pk=id)
	if request.method=='POST':
		partner.delete()
		return redirect('partner_list')
	template_name = 'form/delete_partner_form.html'
	context = {'partner': partner}
	return render(request, template_name, context)

@login_required	
def partner_list(request):
	partner = Partner.objects.order_by('id')
	context = {'partner':partner}
	return render(request, 'partner_list.html', context)

@login_required	
def create_editor(request):
	if request.method=='POST':
		form = EditorForm(request.POST)
		if form.is_valid():
			new_editor = Editor(editor_name=request.POST['editor_name'],
				education=request.POST['education'],
				subject_covers=request.POST['subject_covers'],
				address=request.POST['address'],
				editor_country=request.POST['editor_country'],
				email=request.POST['email'],
				tel=request.POST['tel'],
				rate=request.POST['rate'],
				editor_note=request.POST['editor_note'])
			new_editor.save()
			return redirect('editor_list')
	else:
		form = EditorForm()

	template_name = 'form/create_editor_form.html'
	context = {'form': form}
	return render(request, template_name, context)

@login_required	
def edit_editor(request, id):
	editor = Editor.objects.get(pk=id)
	if request.method=='POST':
		form = EditorForm(request.POST, instance=editor)
		if form.is_valid():
			form.save()
			return redirect('editor_list')
	else:
		form = EditorForm(instance=editor)
	template_name = 'form/edit_editor_form.html'
	context = {'form': form}
	return render(request, template_name, context)

@login_required	
def delete_editor(request, id):
	editor = Editor.objects.get(pk=id)
	if request.method=='POST':
		editor.delete()
		return redirect('editor_list')
	template_name = 'form/delete_editor_form.html'
	context = {'editor': editor}
	return render(request, template_name, context)

@login_required	
def editor_list(request):
	editor = Editor.objects.order_by('id')
	context = {'editor':editor}
	return render(request, 'editor_list.html', context)


@method_decorator(login_required, name='dispatch')
class PartnerView(generic.ListView):
	template_name = 'partner.html'
	context_object_name = 'partner'

	def get_context_data(self, **kwargs):
		# Call the base implementation first to get a context
		context = super(PartnerView, self).get_context_data(**kwargs)

		category_list = Article.objects.distinct().annotate(total_amount_earned=Count('article_title'))

		categories = {}
		letters = []
		for category in category_list:

			if category.catagory in categories:
				count = categories[category.catagory][0]
				new_count = count+1
				categories[category.catagory][0] = new_count
			else:
				categories[category.catagory] = [1,category.catagory]
			letters.append(category.article_title[0])
		count = {}
		context["letters"] = set(letters)
		context['category_list'] = categories 
		context['count_list'] = count
		context['total_article'] = len(category_list)

		return context
	def get_queryset(self):
		cat = self.kwargs.get("cat",None)
		charsort = self.kwargs.get("charsort",None)
		search = self.request.GET.get('search')


		query_set = None
		if cat is not None:
			query_set=Article.objects.filter(catagory=cat).order_by('-id')
		elif charsort is not None:
			query_set=Article.objects.filter(article_title__istartswith=charsort).order_by('-id')
		elif search is not None:
			query_set=Article.objects.filter(article_title__istartswith=search)
		else:
			query_set=Partner.objects.all().order_by('id')
		return query_set

@method_decorator(login_required, name='dispatch')
class EditorView(generic.ListView):
	template_name = 'editor.html'
	context_object_name = 'editor'

	def get_context_data(self, **kwargs):
		# Call the base implementation first to get a context
		context = super(EditorView, self).get_context_data(**kwargs)

		category_list = Article.objects.distinct().annotate(total_amount_earned=Count('article_title'))

		categories = {}
		letters = []
		for category in category_list:

			if category.catagory in categories:
				count = categories[category.catagory][0]
				new_count = count+1
				categories[category.catagory][0] = new_count
			else:
				categories[category.catagory] = [1,category.catagory]
			letters.append(category.article_title[0])
		count = {}
		context["letters"] = set(letters)
		context['category_list'] = categories 
		context['count_list'] = count
		context['total_article'] = len(category_list)

		return context
	def get_queryset(self):
		cat = self.kwargs.get("cat",None)
		charsort = self.kwargs.get("charsort",None)
		search = self.request.GET.get('search')


		query_set = None
		if cat is not None:
			query_set=Article.objects.filter(catagory=cat).order_by('-id')
		elif charsort is not None:
			query_set=Article.objects.filter(article_title__istartswith=charsort).order_by('-id')
		elif search is not None:
			query_set=Article.objects.filter(article_title__istartswith=search)
		else:
			query_set=Editor.objects.all().order_by('id')
		return query_set
