from __future__ import unicode_literals

from django.db import models
from fbstats.users.models import User
from django.contrib.postgres.fields import JSONField
from model_utils.models import TimeStampedModel
from .manager import *

# Create your models here.


class PSYPT(models.Model):
    """Personality Test Category."""

    name = models.TextField(null=False, blank=False)
    short_desc = models.TextField(null=True, blank=True)
    ctitation = models.TextField(null=True, blank=True)
    totalquestions = models.IntegerField(default=20)

    # manager
    objects = PSYPTManager()

    def __str__(self):
        return str(self.name)


class PSYPTDomain(models.Model):
    """Definition for the setup of the test including test identifier and test item identifier."""

    psy_pt = models.ForeignKey(PSYPT)

    domain = models.TextField(null=True, blank=True)
    short_desc = models.TextField(null=False, blank=False)
    long_desc = models.TextField(null=True, blank=True)
    count = models.IntegerField(default=0)

    # manager
    objects = PSYPTDomainManager()
    
    def __str__(self):
        return str(self.domain) + " - " + str(self.psy_pt.name)


class PSYPTFacet(models.Model):
    """Definition for the setup of the test including test identifier and test item identifier."""

    psy_pt_domain = models.ForeignKey(PSYPTDomain)

    facet = models.TextField(null=True, blank=True)
    short_desc = models.TextField(null=False, blank=False)
    long_desc = models.TextField(null=True, blank=True)

    # manager
    objects = PSYPTFacetManager()
    
    def __str__(self):
        return ""


class PSYPTItem(models.Model):
    """Personality Test Item."""

    # Foregin key to PSY_PT_DOMAIN
    psy_pt_domain = models.ForeignKey(PSYPTDomain, null=True, blank=True)

    content = models.TextField(null=False, blank=False)

    # IPIP item number
    item_num_1 = models.TextField(null=False, blank=False)
    
    # IPIP item number
    item_num_2 = models.TextField(null=True, blank=True)
    
    # IPIP item number
    item_num_3 = models.TextField(null=True, blank=True)

    facet = models.TextField(null=True, blank=True)

    # Flag for scoring, e.g. +/-
    keyed = models.TextField(default="+")

    # manager
    objects = PSYPTItemManager()
        
    def __str__(self):
        return str(self.content)


class PSYPTHist(TimeStampedModel):
    """History for Personality Test."""

    user = models.ForeignKey(User)
    completed = models.BooleanField(default=False)
    score = models.IntegerField(default=0)

    # manager
    objects = PSYPTHistManager()

    def __str__(self):
        return str(self.score)


class PSYPTUserAttempt(TimeStampedModel):
    """Definition for the test result."""

    # test
    test = models.ForeignKey(PSYPTHist)

    # item
    psy_pt_item = models.ForeignKey(PSYPTItem)

    # user
    user = models.ForeignKey(User)

    # answer text
    answer = models.TextField(null=True, blank=True)

    # manager
    objects = PSYPTUserAttemptManager()
    
    def __str__(self):
        return str(self.psy_pt_item)


class PSYPTResultDef(models.Model):
    """Definition for the test result."""

    # Low, neutral, high
    score = models.TextField()

    # Test Descriptipn
    score_desc = models.TextField(null=True, blank=True)

    # Foreigin Key to PSYPTDomain
    psy_pt_domain =  models.ForeignKey(PSYPTDomain)
    psy_pt = models.ForeignKey(PSYPT)

    # manager
    objects = PSYPTResultDefManager()
    
    def __str__(self):
        return str(self.score)



    