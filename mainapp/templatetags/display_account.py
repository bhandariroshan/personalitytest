from django import template
register = template.Library()


@register.filter(name='display_account', is_safe=True)
def display_account(field):
    # all_accounts = ['Twitter', 'Facebook']
    all_accounts = ['Facebook']
    for base_account in field:
        acc = base_account.get_provider_account().get_brand()['name']
        all_accounts.remove(acc)
    # parameters = {'all_accounts': all_accounts}
    final_html = ""
    for each in all_accounts:
        final_html += (
            '<a style="margin-bottom: 20px;"'
            ' class="btn btn-block btn-social btn-{0}'
            ' signin-btn" href="/accounts/{0}/login/'
            '?process=connect"><i class="fa'
            ' fa-{0}"></i> Connect {1}</a>'
        ).format(each.lower(), each)
    if not final_html:
        final_html = "<h4>That's all !!</h4>"
    return final_html
