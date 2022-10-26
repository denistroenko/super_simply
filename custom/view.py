from flask import request, session, redirect
import web_forms


# custom views
def mapping_view(app: object, site :object):
    @app.route('/', methods=['POST'])
    @app.route('/<path:page_url>', methods=['POST'])
    def form_completed(page_url: str=''):
        forms = web_forms.get_forms()
        feedback_form = forms['feedback']

        session['name'] = feedback_form.name.data
        session['second_name'] = feedback_form.second_name.data
        session['last_name'] = feedback_form.last_name.data
        session['phone'] = feedback_form.phone.data
        session['email'] = feedback_form.email.data
        session['message'] = feedback_form.message.data
        session['page_url'] = feedback_form.page_url.data
        session['page_name'] = feedback_form.page_name.data
        session['choice'] = feedback_form.choice.data

        # ВСТАВИТЬ СЮДА ОБРАБОТКУ ФОРМЫ

        return redirect('/_form_completed')
