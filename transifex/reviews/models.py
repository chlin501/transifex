"""
This module contains a model representation
of the review request. The following definitions are used:

POReviewRequest: A file under review entry in the database.
"""

import os
from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _

from projects.models import Component
from transifex.translations.models import POFile 

class POReviewRequestManager(models.Manager):

    def open_reviews(self):
        """ Return a list of active Requests. """
        return self.filter(status='O')

    def closed_reviews(self):
        """ Return a list of inactive Requests. """
        return self.filter(status='C')

class POReviewRequest(models.Model):
    """A POReviewRequest is a review representation of a PO file.
    
    The review refers to a specific PO file. It can have two statuses:
    "open" or "closed". By default the PO review is created as "open".
    The reviewer marks it as "closed", if he accepted or rejected the 
    translation. This is indicated to the resolution field.
    When a reviewer approves the translation, the review resolution takes 
    the values 'Accepted'. Otherwise, if he wants to reject it, 
    it is marked as 'Rejected'. The resolution 'Null' vakue is used as 
    the default. The po file can also be commented and the comments are 
    stored in this model.
     
    """
    
    STATUS_CHOICES = (('O', 'Open'),
                     ('C', 'Closed'),)

    RESOLUTION_CHOICES = (('N', 'Null'),
                     ('A', 'Accepted'),
                     ('R', 'Rejected'),)

    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='O',
        help_text="The review's status (open, closed, etc.)")
    resolution = models.CharField(max_length=1, choices=RESOLUTION_CHOICES,
        default='N', help_text="The review's resolution/closing state.")
    created_on = models.DateTimeField(auto_now_add=True,
        help_text="Date and time of creation")
    last_updated = models.DateTimeField(auto_now=True,
        help_text="Date and time of last update")

    file_name = models.CharField(max_length=200, editable=False,
        help_text="The review file name")

    # Relations
    component = models.ForeignKey(Component, verbose_name=_('Component'),
                                  related_name='reviews')
#    pofile = models.ForeignKey(POFile, verbose_name=_('PO File'),
#                               related_name='reviews',)
    author = models.ForeignKey(User)

    # Managers
    objects = POReviewRequestManager()

    def __unicode__(self):
        return u"%(component)s (%(id)s)" % {
            'component': self.component,
            'id': self.id,
            }

    class Meta:
        verbose_name = _('Review Request')
        verbose_name_plural = _('Review Requests')
        ordering  = ('-created_on',)
        get_latest_by = 'created_on'


    @property
    def is_closed(self):
        return (self.status == 'C')

    @property
    def is_open(self):
        return (self.status == 'O')

    @property
    def full_review_filename(self):
        return '%d.%s' % (self.id, self.file_name)
        
    @property
    def file_url(self):
        return settings.REVIEWS_URL + self.full_review_filename

    
