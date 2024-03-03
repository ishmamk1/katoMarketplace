from django.shortcuts import render, get_object_or_404, redirect
from .models import Category, Item, ConversationMessage, Conversation
from .forms import SignUp, NewItem, EditItem, MessageForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as auth_logout
from django.db.models import Q
# Create your views here.

"""

"""
def index(request):
    """
    The index function is the main page of the website. It displays a list of
    categories and items that are currently for sale, including the user's items.

    :param request: Get the request from the user
    :return: A list of categories and a list of items
    """
    categories = Category.objects.all()
    items = Item.objects.filter(isSold=False)[0:6]
    return render(request, 'app/index.html', {
        'categories' : categories,
        'items' : items,
    })

def contact(request):
    return render(request, 'app/contact.html')

def about(request):
    return render(request, 'app/about.html')

def privacy(request):
    return render(request, 'app/privacy.html')

def terms(request):
    return render(request, 'app/tos.html')

def detail(request, pk):
    """
    The detail function is used to display the details of a specific item.
    It takes in a request and an item id (pk), then returns the detail page for that
    item. It also gets three related items (items with the same category as this one)
    to display on the side.

    :param request: Get the request from the user
    :param pk: Get the item from the database
    :return: The detail
    """
    item = get_object_or_404(Item, pk=pk)
    relatedItems = Item.objects.filter(category=item.category, isSold=False).exclude(pk=pk)[0:3]

    return render(request, 'app/detail.html', {
        'item' : item,
        'relatedItems': relatedItems,
    })

def signUp(request):
    """
    Handles user sign-up functionality.

    This view function manages the user sign-up process. It checks if the HTTP request method is POST,
    processes the form data, and creates a new user account upon successful validation. If the method is not POST,
    it initializes an empty sign-up form to render on the template.

    :param request (HttpRequest): The HTTP request object containing user data.

    :return HttpResponse: A redirect to the login page upon successful sign-up or a rendered signup page with the form.
    """
    if request.method == 'POST':
        form = SignUp(request.POST)

        if form.is_valid():
            form.save()

            return redirect('/login/')
    else:
        form = SignUp()

    return render(request, 'app/signup.html', {
        'form' : form
    })

@login_required
def new(request):
    """
    Handles the creation of a new item (name, category, image, description) by a logged-in user.

    :param request {HttpRequest) : The HTTP request object containing user data.

    :return (HttpResponse) : A redirect to the item detail view upon successful item creation or a rendered form page with the item creation form.

    Notes:
        - The 'app/form.html' template should be created to render the item creation form.
        - The @login_required decorator ensures that only authenticated users can access this view.
    """
    if request.method == 'POST':
        form = NewItem(request.POST, request.FILES)

        if form.is_valid():
            item = form.save(commit=False)
            item.owner = request.user
            item.save()

            return redirect('item:detail', pk=item.id)
    else:
        form = NewItem()

    return render(request, 'app/form.html', {
        'form' : form,
        'title' : 'New Item',
    })

@login_required
def dashboard(request):
    """
    Displays the dashboard of items owned by the logged-in user.

    :param request (HttpRequest): The HTTP request object containing user data.

    :return (HttpResponse): A rendered dashboard page displaying items owned by the user.

    Notes:
        - The 'app/dashboard.html' template should be created to render the user's dashboard.
        - The @login_required decorator ensures that only authenticated users can access this view.
    """
    items = Item.objects.filter(owner=request.user)

    return render(request, 'app/dashboard.html',{
        'items' : items,
    })

@login_required
def delete(request,pk):
    """
        Deletes an item belonging to the authenticated user.

        :param request (HttpRequest): An HTTP request object containing metadata and data about the user's request.
        :param pk (int): The primary key of the item to be deleted.

        :return: An HttpResponse that redirects the user to the 'item:index' URL after successfully deleting the item.

        :raises Http404: If the item with the specified primary key does not exist or does not belong to the authenticated user.

        This view function deletes an item based on the provided primary key (pk) if the item exists and belongs to the currently authenticated user.
    """
    item = get_object_or_404(Item, pk=pk, owner=request.user)
    item.delete()
    return redirect('item:index')

@login_required
def edit(request, pk):
    """
        Edits an item belonging to the authenticated user using the EditItem form.

        :param request (HttpRequest): An HTTP request object containing metadata and data about the user's request.
        :param pk (int): The primary key of the item to be edited.

        :return: If the HTTP request method is POST and the form data is valid, redirects the user to the item's detail page.
        :return: If the HTTP request method is not POST, renders the item edit form template.

        This view function allows an authenticated user to edit an item based on the provided primary key (pk) if the item exists and belongs to the user.
        The user is presented with a form to modify item details. If the form is valid, the item is saved and the user is redirected to the detail page of the edited item.
        The 'app/form.html' template is used for rendering the edit form.
    """
    item = get_object_or_404(Item, pk=pk, owner=request.user)

    if request.method == 'POST':
        form = EditItem(request.POST, request.FILES, instance=item)

        if form.is_valid():
            item.save()

            return redirect('item:detail', pk=item.id)
    else:
        form = EditItem(instance=item)

    return render(request, 'app/form.html', {
        'form' : form,
        'title' : 'Edit Item',
    })

def search(request):
    """
        Performs a search for items in the online marketplace through the input given in the search bar.

        :param request (HttpRequest): An HTTP request object containing metadata and data about the user's search request.

        :return: Renders the 'app/search.html' template with search results, query, categories, and selected category for filtering.

        This view function handles item search functionality in the online marketplace. Users can search for items by entering a query and optionally selecting a category for filtering.
        The search query is obtained from the GET request parameter 'query'. Items that are not marked as sold (isSold=False) are considered for the search.
        Users can further filter the results by category, which is obtained from the GET request parameter 'category'. If a category is selected, the search is narrowed down to items within that category.
        The 'name' and 'description' fields of items are searched for the query using a case-insensitive contains match.
        """
    query = request.GET.get('query', '')
    items = Item.objects.filter(isSold=False)
    categories = Category.objects.all()
    category_id = request.GET.get('category', 0)

    if category_id:
        items = items.filter(category_id=category_id)

    if query:
        items = items.filter(name__icontains=query or Q(description__icontains=query))


    return render(request, 'app/search.html', {
        'items' : items,
        'query' : query,
        'categories' : categories,
        'category_id' : int(category_id),
    })

@login_required()
def newConversation(request, item_pk):
    """
        Initiates a new conversation for an item between users.

        :param request (HttpRequest): An HTTP request object containing metadata and data about the user's request.
        :param item_pk (int): The primary key of the item for which a new conversation is initiated.

        :return: If the user is the owner of the item, redirects to the item's dashboard.
        :return: If a conversation already exists for the item and the user, redirects to the existing conversation's information page.
        :return: If the HTTP request method is POST and the form data is valid, creates a new conversation and a message, and redirects to the item's detail page.
        :return: If the HTTP request method is not POST, renders the conversation form template.

        This view function allows users to initiate a new conversation related to a specific item. If the user is the owner of the item, they are redirected to the item's dashboard.
        If a conversation already exists for the item and the user, the user is redirected to the information page of the existing conversation.
        Users can send messages through the conversation form, which is processed when the form is submitted as a POST request.
        A conversation is created, and the initial message is saved, connecting the participants (user and item owner).
        The 'app/conversation.html' template is used for rendering the conversation form.
    """
    item = get_object_or_404(Item, pk=item_pk)

    if item.owner == request.user:
        return redirect('item:dashboard')

    conversations = Conversation.objects.filter(item=item).filter(members__in=[request.user.id])

    if conversations:
        return redirect('item:info', pk=conversations.first().id)

    if request.method == 'POST':
        form = MessageForm(request.POST)

        if form.is_valid():
            conversation = Conversation.objects.create(item=item)
            conversation.members.add(request.user)
            conversation.members.add(item.owner)
            conversation.save()

            conversationMessage = form.save(commit=False)
            conversationMessage.conversation = conversation
            conversationMessage.host = request.user
            conversationMessage.save()

            return redirect('item:detail', pk=item_pk)
    else:
        form = MessageForm()

    return render(request, 'app/conversation.html', {'form': form, 'item': item})

@login_required()
def inbox(request):
    """
        Displays the user's inbox containing conversations.

        :param request (HttpRequest): An HTTP request object containing metadata and data about the user's request.

        :return: Renders the 'app/inbox.html' template with the user's conversations.

        This view function displays the user's inbox, which contains conversations they are part of.
        Conversations are retrieved from the database based on the currently authenticated user.
        The 'app/inbox.html' template is used for rendering the inbox, showing a list of conversations the user is a member of.

    """
    conversations = Conversation.objects.filter(members__in=[request.user.id])

    return render(request, 'app/inbox.html', {
        'conversations' : conversations,
    })

@login_required()
def detailInfo(request,pk):
    """
        Displays detailed information and messages for a specific conversation.

        :param request (HttpRequest): An HTTP request object containing metadata and data about the user's request.
        :param pk (int): The primary key of the conversation for which detailed information is displayed.

        :return: If the HTTP request method is POST and the form data is valid, saves a new message and redirects to the conversation's detail information page.
        :return: If the HTTP request method is not POST, renders the 'app/detailInfo.html' template with conversation details and messages.

        This view function displays detailed information for a specific conversation in the user's inbox.
        The conversation is retrieved based on the provided primary key (pk) and the currently authenticated user.
        Users can send messages through the conversation using a form, which is processed when the form is submitted as a POST request.
        The conversation message is associated with the conversation and saved along with the user as the host.
        The 'app/detailInfo.html' template is used for rendering the conversation details and messages.

    """
    conversation = Conversation.objects.filter(members__in=[request.user.id]).get(pk=pk)

    if request.method == 'POST':
        form = MessageForm(request.POST)

        if form.is_valid():
            conversationMsg = form.save(commit=False)
            conversationMsg.conversation = conversation
            conversationMsg.host = request.user
            conversationMsg.save()

            return redirect('item:info', pk=pk)
    else:
        form = MessageForm()

    return render(request, 'app/detailInfo.html', {
        'conversation' : conversation,
        'form' : form,
    })

@login_required()
def logout(request):
    auth_logout(request)
    return render(request, 'app/index.html')




