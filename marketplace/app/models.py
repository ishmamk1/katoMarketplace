from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Category(models.Model):
    """
        Model representing a category for items.

        Attributes:
            name (CharField): The name of the category.

        Meta Options:
            ordering (tuple): Orders categories by name.
            verbose_name_plural (str): Changes the verbose name plural to 'Categories'.

        Methods:
            __str__(): Returns a string representation of the category.
        """
    name = models.CharField(max_length=200)

    # Change name to Categories and name item in db as name.
    class Meta:
        ordering = ('name', )
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name

class Item(models.Model):
    """
        Model representing an item in the online marketplace.

        Attributes:
            category (ForeignKey): The category to which the item belongs.
            name (CharField): The name of the item.
            description (TextField): A description of the item (optional).
            price (FloatField): The price of the item.
            image (ImageField): An image representing the item (optional).
            owner (ForeignKey): The user who owns the item.
            isSold (BooleanField): Indicates whether the item is sold or not.
            createdAt (DateTimeField): The timestamp when the item was created.

        Meta Options:
            ordering (tuple): Orders items by name.
            verbose_name_plural (str): Changes the verbose name plural to 'Items'.

        Methods:
            __str__(): Returns a string representation of the item.
        """
    category = models.ForeignKey(Category, related_name='items', on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True, max_length=500)
    price = models.FloatField()
    image = models.ImageField(upload_to='itemImages', blank=True, null=True)
    owner = models.ForeignKey(User, related_name='items', on_delete=models.CASCADE)
    isSold = models.BooleanField(default=False)
    createdAt = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('name', )
        verbose_name_plural = 'Items'

    def __str__(self):
        return self.name

class Conversation(models.Model):
    """
        Model representing a conversation related to an item.

        Attributes:
            item (ForeignKey): The item associated with the conversation.
            members (ManyToManyField): Users participating in the conversation.
            createdAt (DateTimeField): The timestamp when the conversation was created.
            modifiedAt (DateTimeField): The timestamp when the conversation was last modified.

        Meta Options:
            ordering (tuple): Orders conversations by the most recent modification.

    """
    item = models.ForeignKey(Item, related_name='conversations', on_delete=models.CASCADE)
    members = models.ManyToManyField(User, related_name='conversations')
    createdAt = models.DateTimeField(auto_now_add=True)
    modifiedAt = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-modifiedAt',)

class ConversationMessage(models.Model):
    """
        Model representing a message within a conversation.

        Attributes:
            conversation (ForeignKey): The conversation to which the message belongs.
            content (TextField): The content of the message.
            createdAt (DateTimeField): The timestamp when the message was created.
            host (ForeignKey): The user who sent the message.
    """
    conversation = models.ForeignKey(Conversation, related_name='messages', on_delete=models.CASCADE)
    content = models.TextField()
    createdAt = models.DateTimeField(auto_now_add=True)
    host = models.ForeignKey(User, related_name='host', on_delete=models.CASCADE)

