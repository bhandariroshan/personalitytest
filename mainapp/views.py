# -*- coding: utf-8 -*-
import json
from django.views.generic import View
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
import facebook
from allauth.socialaccount.models import SocialToken, SocialApp
from action.models import UserData
from .pull_likes import get_myfacebook_likes
import requests
import sys
import csv
from mainapp.models import (
    PSYPTItem,
    PSYPTUserAttempt,
    PSYPT,
    PSYPTDomain,
    PSYPTHist,
    PSYPTResultDef
)

import random
from django.db.models import Q
from .questions import questions
from django.http import JsonResponse
from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator


class HomeView(View):
    """docstring for HomeView"""
    """Module for previewing data from facebook."""
    template_name = 'landing.html'


    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            return HttpResponseRedirect('/load/')
        else:
            return render(request, self.template_name, {})
        
class LoadQuestions(LoginRequiredMixin ,View):

    def get(self, request, *args, **kwargs):
        pt = PSYPT()
        pt.name = 'MINI-IPIP'
        pt.short_desc = 'MINI-IPIP'
        pt.ctitation = 'MINI-IPIP'
        pt.save()

        pd = PSYPTDomain()
        pd.psy_pt = PSYPT.objects.filter()[0]
        pd.domain = 'O'
        pd.short_desc = 'Openness to experience'
        pd.save()

        pd = PSYPTDomain()
        pd.psy_pt = PSYPT.objects.filter()[0]
        pd.domain = 'C'
        pd.short_desc = 'Conscientiousness'
        pd.save()

        pd = PSYPTDomain()
        pd.psy_pt = PSYPT.objects.filter()[0]
        pd.domain = 'E'
        pd.short_desc = 'Extraversion'
        pd.save()

        pd = PSYPTDomain()
        pd.psy_pt = PSYPT.objects.filter()[0]
        pd.domain = 'A'
        pd.short_desc = 'Agreeableness'
        pd.save()

        pd = PSYPTDomain()
        pd.psy_pt = PSYPT.objects.filter()[0]
        pd.domain = 'N'
        pd.short_desc = 'Neuroticism'
        pd.save()

        for each_question in questions:
            pi = PSYPTItem()
            try:
                pi.content = each_question.split(',')[0]
                pi.item_num_1 = each_question.split(',')[1]
                pi.save()
            except:
                pass

        return HttpResponseRedirect('/')


class TestView(LoginRequiredMixin, View):
    """Taking Test."""

    template_name = 'test.html'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(TestView, self).dispatch(request, *args, **kwargs)

    def  get_question(self, request, nextquest, questionid, optionselected):
        redirect = False
        ''' 
        ----------------------- Start of Algorithm  ---------------------------------   
            # Exam Generation
            1. Check user incomplete exam
            2. If there is incomplete exam, serve the exam
            3. Else Generate a new exam and serve exam

            # Saving Attempts
            1. If attempted answer for question id is '' and for the same question id and exam id saved answer is not empty
                then do not override
            2. Else override attempted asnwer

            # Calculating Result
            1. On exam completion, get all the answers and keyed values and find result on each domain
            2. Save score

         ----------------------- End of Algorithm ------------------------------------ 
         '''
        # Step 1:: Generate or Get Exam
        
        exam  = PSYPTHist.objects.get_or_create(
            completed=False,
            user=request.user
        )
        
        # Get and save attempt of user
        if questionid != '':
            userattempt = PSYPTUserAttempt.objects.filter(
                user=request.user,
                psy_pt_item__id=int(questionid),
                test=exam[0]
            )

            if optionselected != '' and userattempt:
                userattempt[0].answer=optionselected
            
            if userattempt:
                userattempt[0].save()
                
        
        # Step 2:: Question Generation
        #   1. Generate 20 or test based question for Mini Test
        #   2. Make sure it has all O C E A N domain questions 
        #   3. Make sure the questions keyed (+/-) distribution for questions are equal
        #   4. Make sure the 
        #   5. Attach exam id for the generated questions
        #   6. Save attempts
        #   7. If all 20 questions has been answered, then mark exam id as completed and redirect to results page


        # CHECK EXAM HAS BEEN COMPLETED OR NOT
        attempt_count = PSYPTUserAttempt.objects.filter(
            answer__isnull=False,
            user=request.user,
            test=exam[0]
        ).count()

        # Count the number of questions, based on test
        psypt = PSYPT.objects.filter()[0]

        # psyptt domains
        domains = PSYPTDomain.objects.filter(psy_pt=psypt)

        qids = PSYPTItem.objects.filter(psy_pt_domain__in=domains).values('id').distinct()
        questionids = []
        for eachid in qids:
            if eachid not in questionids:
                questionids.append(eachid['id'])
        totalquestions = len(questionids)

        print("Total Questions:: ", totalquestions)
        print("Attempt Count:: ", attempt_count)

        # If there are 20 answers, mark the exam as completed, redirect to results page
        if attempt_count >= totalquestions:
            exam[0].completed = True
            exam[0].save()
            redirect = True
            return (redirect, None, None, None, exam[0].id)

        exam[0].save()

        percentage = attempt_count / totalquestions * 100
        
        if nextquest < 1:
            nextquest = 0
        if nextquest >= totalquestions:
            nextquest = totalquestions - 1

        # If last question and there are other unanswered questions, fetch one unaswered and serve that
        unattemted  = PSYPTUserAttempt.objects.filter(
            user=request.user,
            test=exam[0],
            answer__isnull=True
        )

        if nextquest <= totalquestions and unattemted:
            # serve unattempted question
            question = unattemted[0].psy_pt_item
        else:
            # Generate question, algorithm implementation here
            #  1. Get a Category i.e Domain 
            #  2. Count questions of the category in attempts
            #  3. If count > total questions to be selected from the category, select another category
            #  4. Generate a new question
            #  5. Repeat steps 2 to 4 until we get total questions

            # filter for different exam

            unwanted_objects = PSYPTUserAttempt.objects.filter(
                user=request.user,
                test=exam[0]
            )

            unwanted_list = [o.psy_pt_item.id for o in unwanted_objects]

            difflist = set(questionids) - set(unwanted_list)
            questions = PSYPTItem.objects.filter(
                id=difflist.pop()
            )
            question = questions[0]

        # Create attempt for question
        qt = PSYPTUserAttempt.objects.get_or_create(
            user=request.user,
            psy_pt_item=question,
            test=exam[0]
        )
        qt[0].save()

        return (redirect, nextquest, percentage, question, exam[0].id)

    def get(self, request, *args, **kwargs):
        nextquest = int(request.GET.get('next', 0))
        optionselected = request.GET.get('optionselected', '')
        questionid = request.GET.get('questionid','')

        redirect, nextquest, percentage, question, examid = self.get_question(
            request, 
            nextquest, 
            questionid, 
            optionselected
        )

        if redirect:
            return HttpResponseRedirect('/result/' + str(examid))

        return render(
            request, 
            self.template_name, 
            {
                'question': question, 
                'qno': nextquest,
                'qid': question.id,
                'percentage': percentage
            }, 
            RequestContext(request, {})
        )

    def post(self, request, *args, **kwargs):
        nextquest = int(request.POST.get('next', 0))
        optionselected = request.POST.get('optionselected', '')
        questionid = request.POST.get('questionid','')
        redirect, nextquest, percentage, question, examid = self.get_question(
            request, 
            nextquest, 
            questionid, 
            optionselected
        )
        if redirect:
            return JsonResponse({'url': '/result/' + str(examid) + '/', 'status': 'redirect'})
        else:
            return JsonResponse({
                'status': 'ok',
                'question': question.content, 
                'qno': nextquest,
                'qid': question.id,
                'percentage': percentage
            })

class LoadUserLikes(LoginRequiredMixin, View):
    """Module for previewing data from facebook."""
    template_name = 'load.html'

    def get_context_data(self, **kwargs):
        context = {}
        tokens = SocialToken.objects.filter(
            account__user=self.request.user,
            account__provider='facebook'
        )
        if tokens:
            context['token'] = tokens[0].token

        fb_app = get_object_or_404(SocialApp, id=1)
        context['app_id'] = fb_app.client_id
        return context

    def get(self, request, *args, **kwargs):
        tokens = SocialToken.objects.filter(
            account__user=request.user,
            account__provider='facebook'
        )

        user_data = UserData.objects.get_or_create(user=request.user)
        user_data[0].save()

        # myfbgraph = facebook.GraphAPI(tokens[0].token)
        # my_likes = get_myfacebook_likes(myfbgraph, request.user)
        # user_data[0].likes = my_likes
        # user_data[0].save()

        return render(request, self.template_name, self.get_context_data())


class ResultView(LoginRequiredMixin, View):
    """docstring for HomeView"""
    """Module for previewing data from facebook."""
    template_name = 'result.html'


    def get(self, request, testid, *args, **kwargs):
        
        exam = PSYPTHist.objects.get(id=int(testid))
        
        domains = PSYPTDomain.objects.filter()
        domain_scores = {}

        for each_domain in domains:
            domain_scores[each_domain.id] = {
                'domainScore': 0,
                'name': each_domain.domain,
                'totalScore': 0
            }

        answer_text = []

        testanswers = PSYPTUserAttempt.objects.filter(
            user=request.user,
            test__id=int(testid),
            psy_pt_item__psy_pt_domain=each_domain
        )


        for each_answer in testanswers:
            for each_domain in each_answer.psy_pt_item.psy_pt_domain.all():
                try:
                    if each_answer.psy_pt_item.keyed == '+':
                        domain_scores[each_domain.id]['domainScore'] += int(each_answer.answer) + 1
                        domain_scores[each_domain.id]['totalScore'] += 5
                    else:
                        domain_scores[each_domain.id]['domainScore'] += 5-int(each_answer.answer)
                        domain_scores[each_domain.id]['totalScore'] += 5
                except:
                    domain_scores[each_domain.id]['domainScore'] += 0
                    domain_scores[each_domain.id]['totalScore'] += 0


        # Score categorization and result display dynamic here
        score = PSYPTResultDef.objects.filter()
        if score:
            answer_text.append(score[0].score_desc)
        else:
            answer_text.append("Openness measures your ability.")

        sendScore = []
        for each_domain in domains:
            try:
                scor = domain_scores[each_domain.id]['domainScore']/domain_scores[each_domain.id]['totalScore']*100
                sendScore.append(
                    [
                        each_domain.short_desc, 
                        "{0:.2f}".format(round(scor,2))
                    ]
                )
            except:
                sendScore.append([each_domain.short_desc, 0])

        return render(request, self.template_name, {'scores':sendScore, 'text': answer_text})
