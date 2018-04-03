from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, TextAreaField, SelectField, FileField, SubmitField
from wtforms.validators import InputRequired, Email, Length, EqualTo


class LoginForm(FlaskForm):
    email_username = StringField("Correu electrònic o nom d'usuari", [
        InputRequired(),
        Length(min=4, max=254)
    ])
    password = PasswordField("Contrasenya", [
        InputRequired(),
        Length(min=8, max=80)
    ])
    remember = BooleanField("Recordar la sessió")

class RegisterForm(FlaskForm):
    name = StringField("Nom", [
        InputRequired(message=("Has d'escriure un nom")),
        Length(min=2, max=40, message=("El nom ha d'estar entre els 2 i els 40 caràcters"))
    ])
    username = StringField("Nom d'usuari", [
        InputRequired(message=("Has d'escriure un nom d'usuari")),
        Length(min=4, max=20, message=("El nom d'usuari ha d'estar entre els 4 i els 20 caràcters"))
    ])
    bio = TextAreaField("Biografia (opcional)", [
        Length(max=240, message=("La biografia no pot passar dels 240 caràcters"))
    ])
    email = StringField("Correu electrònic", [
        InputRequired(message=("Has d'escriure un correu")),
        Email(message=("El correu ha de ser vàlid")),
        Length(min=4, max=254, message=("El correu ha d'estar entre els 4 i els 254 caràcters"))
    ])
    tdr_file = FileField("PDF del teu TDR", [
        InputRequired(message=("El PDF del teu TDR és necessari"))
    ])
    tdr_title = StringField("Títol del teu TDR", [
        InputRequired(message=("Has d'escriure el títol del teu TDR")),
        Length(min=2, max=60, message=("El títol del teu TDR ha d'estar entre els 2 i els 60 caràcters"))
    ])
    tdr_description = TextAreaField("Descripció del teu TDR", [
        InputRequired(message=("Has d'escriure la descripció del teu TDR")),
        Length(min=15, max=500, message=("La descripció del teu TDR ha d'estar entre els 15 i els 500 caràcters"))
    ])
    tdr_subject = SelectField(
        "Àmbit del teu TDR",
        choices=[
            ("Altres", "Altres"),
            ("Biologia", "Biologia"),
            ("Economia i emprenedoria", "Economia i emprenedoria"),
            ("Educació artística, musical, visual i plàstica", "Educació artística, musical, visual i plàstica"),
            ("Educació física", "Educació física"),
            ("Física", "Física"),
            ("Història", "Història"),
            ("Humanitats", "Humanitats"),
            ("Tecnologia", "Tecnologia"),
            ("Llengua estrangera", "Llengua estrangera"),
            ("Llengua i literatura", "Llengua i literatura"),
            ("Matemàtiques", "Matemàtiques"),
            ("Química", "Química"),
            ("Religió", "Religió")
        ]
    )
    tdr_year = SelectField(
        "Promoció del teu TDR",
        choices=[
            ("2017 - 2018", "2017 - 2018"),
            ("2015 - 2016", "2015 - 2016"),
            ("2013 - 2014", "2013 - 2014"),
            ("2011 - 2012", "2011 - 2012"),
            ("2009 - 2010", "2009 - 2010"),
            ("2007 - 2008", "2007 - 2008"),
            ("2005 - 2006", "2005 - 2006")
        ]
    )
    password = PasswordField("Contrasenya", [
        InputRequired(message=("Has d'escriure una contrasenya")),
        Length(min=8, max=80, message=("La contrasenya ha d'estar entre els 8 i els 80 caràcters"))
    ])
    confirmPassword = PasswordField("Confirmar contrasenya", [
        EqualTo('password', message=("Las contrasenyas han de coincidir"))
    ])
    remember = BooleanField("Recordar la sessió")

class editUserForm(FlaskForm):
    bio = TextAreaField("Biografia (opcional)", [
        Length(max=240, message=("La biografia no pot passar dels 240 caràcters"))
    ])
    submitEditUser = SubmitField("Editar perfil")

class deleteUserForm(FlaskForm):
    password = PasswordField("Contrasenya de confirmació", [
        InputRequired(),
        Length(min=8, max=80)
    ])
    submitDeleteUser = SubmitField("Si, vull eliminar el meu perfil")

class VerifyForm(FlaskForm):
    school = StringField("Centre educatiu", [
        InputRequired(message="Has d'escriure un centre educatiu"),
        Length(min=4, max=120, message=("El nom del centre educatiu ha d'estar entre els 4 i els 120 caràcters"))
    ])
    email = StringField("Correu de l'usuari creador del treball", [
        InputRequired(message="Has d'escriure el correu del creador del treball"),
        Email(message=("No existeix cap usuari amb aquest correu")),
        Length(min=4, max=254, message="No existeix cap usuari amb aquest correu")
    ])
    mark = SelectField(
        "Nota del treball sobre 10",
        choices=[
            ("1", "1"),
            ("2", "2"),
            ("3", "3"),
            ("4", "4"),
            ("5", "5"),
            ("6", "6"),
            ("7", "7"),
            ("8", "8"),
            ("9", "9"),
            ("10", "10")
        ]
    )
    mantra = PasswordField("Mantra", [
        InputRequired(message="Aquest mantra no és vàlid"),
        Length(min=4, max=80, message="Aquest mantra no és vàlid")
    ])

class searchTDRForm(FlaskForm):
    title = StringField("Títol del TDR", [
        Length(max=60)
    ])
    subject = SelectField(
        "Àmbit del TDR",
        choices=[
            ("", "No especificar"),
            ("Altres", "Altres"),
            ("Biologia", "Biologia"),
            ("Economia i emprenedoria", "Economia i emprenedoria"),
            ("Educació artística, musical, visual i plàstica", "Educació artística, musical, visual i plàstica"),
            ("Educació física", "Educació física"),
            ("Física", "Física"),
            ("Història", "Història"),
            ("Humanitats", "Humanitats"),
            ("Tecnologia", "Tecnologia"),
            ("Llengua estrangera", "Llengua estrangera"),
            ("Llengua i literatura", "Llengua i literatura"),
            ("Matemàtiques", "Matemàtiques"),
            ("Química", "Química"),
            ("Religió", "Religió")
        ]
    )
    year = SelectField(
        "Promoció del TDR",
        choices=[
            ("", "No especificar"),
            ("2017 - 2018", "2017 - 2018"),
            ("2015 - 2016", "2015 - 2016"),
            ("2013 - 2014", "2013 - 2014"),
            ("2011 - 2012", "2011 - 2012"),
            ("2009 - 2010", "2009 - 2010"),
            ("2007 - 2008", "2007 - 2008"),
            ("2005 - 2006", "2005 - 2006")
        ]
    )
    verifiedOnly = BooleanField("Només mostrar treballs verificats")
    submitSearchTDR = SubmitField("Buscar per TDR")

class searchUserForm(FlaskForm):
    username = StringField("Nom d'usuari de l'alumne", [
        Length(max=20)
    ])
    submitSearchUser = SubmitField("Buscar per usuari")
