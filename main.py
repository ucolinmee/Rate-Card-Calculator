from flask import Flask, render_template, request, redirect, url_for
from flask_wtf import FlaskForm
from flask_bootstrap import Bootstrap
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired
from rate_card import Ratecard

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap(app)
ratecard = Ratecard()


class RatesForm(FlaskForm):
    package_selected = SelectField('Select Package Size',
                                   choices=[('17,800', '17,800'), ('35,244', '35,244'),
                                            ('52,332', '52,332'), ('69,094', '69,094')], validators=[DataRequired()])
    storytell = StringField('Storytell Percentage', validators=[DataRequired()])
    amplify = StringField('Amplify Percentage', validators=[DataRequired()])
    uncut = StringField('Uncut Percentage', validators=[DataRequired()])
    submit = SubmitField('Calculate')


@app.route("/", methods=["GET", "POST"])
def home():
    form = RatesForm()
    if form.validate_on_submit():
        package_selected = form.package_selected.data
        full_budget = int(package_selected.replace(",", ""))
        storytell_pct = int(form.storytell.data) / 100
        amplify_pct = int(form.amplify.data) / 100
        uncut_pct = int(form.uncut.data) / 100

        story_budget = int(full_budget * storytell_pct)
        story_outreach = int(ratecard.packages[package_selected]["storytell"]["outreach"] * storytell_pct)
        story_cont_lower = int(ratecard.packages[package_selected]["storytell"]["content_lower"] * storytell_pct)
        story_cont_higher = int(ratecard.packages[package_selected]["storytell"]["content_higher"] * storytell_pct)

        amplify_budget = int(full_budget * amplify_pct)
        amplify_impressions = int(ratecard.packages[package_selected]["amplify"]["impressions"] * amplify_pct)
        amplify_content = int(ratecard.packages[package_selected]["amplify"]["content"] * amplify_pct)

        uncut_budget = int(full_budget * uncut_pct)
        uncut_lower = int(ratecard.packages[package_selected]["uncut"]["content_lower"] * uncut_pct)
        uncut_higher = int(ratecard.packages[package_selected]["uncut"]["content_higher"] * uncut_pct)

        return render_template("rate-card.html", storytell_pct=form.storytell.data, amplify_pct=form.amplify.data, uncut_pct=form.uncut.data,
                               story_budget=story_budget, story_outreach=story_outreach, story_cont_lower=story_cont_lower, story_cont_higher=story_cont_higher,
                               amplify_budget=amplify_budget, amplify_impressions=amplify_impressions, amplify_content=amplify_content,
                               uncut_budget=uncut_budget, uncut_lower=uncut_lower, uncut_higher=uncut_higher)
    return render_template("test.html", form=form)

#
# @app.route("/edit", methods=["POST"])
# def edit_form():
#     form = RatesForm()
#     if form.validate_on_submit():
#         return render_template("rate-card.html")
#     return render_template("test.html", form=form)
#
#
@app.route('/rate-card', methods=["POST"])
def receive_data():
    # form = RatesForm()
    # if form.validate_on_submit():
    #     storytell_pct = form.storytell.data
    #     story_outreach = ratecard.story_outreach * storytell_pct
    #     amplify_pct = form.amplify.data
    #     uncut_pct = form.uncut.data
    return render_template("rate-card.html")
    # storytell_pct=storytell_pct, amplify_pct=amplify_pct,
    #                         uncut_pct=uncut_pct, story_outreach=story_outreach)



if __name__ == "__main__":
    app.run(debug=True)







































