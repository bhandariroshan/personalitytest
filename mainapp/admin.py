from django.contrib import admin

# from .models import FacebookPost
# admin.site.register(FacebookPost)


from .models import(
	PSYPT,
	PSYPTDomain,
	PSYPTFacet,
	PSYPTItem,
	PSYPTHist,
	PSYPTUserAttempt,
	PSYPTResultDef
)

admin.site.register(PSYPTFacet)
admin.site.register(PSYPTHist)
admin.site.register(PSYPTUserAttempt)


@admin.register(PSYPT)
class PSYPTAdmin(admin.ModelAdmin):
    list_display = (
        "name", "short_desc", "totalquestions"
    )


@admin.register(PSYPTDomain)
class PSYPTDomainAdmin(admin.ModelAdmin):
    list_display = (
        "psy_pt", "domain", "count"
    )


@admin.register(PSYPTItem)
class PSYPTItemAdmin(admin.ModelAdmin):
    list_display = (
       "content", "psy_pt_domain",  "item_num_1", "keyed"
    )

@admin.register(PSYPTResultDef)
class PSYPTItemAdmin(admin.ModelAdmin):
    list_display = (
       "score", "psy_pt_domain",  "score_desc"
    )
