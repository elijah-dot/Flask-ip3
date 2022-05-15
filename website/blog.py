from flask import Blueprint,render_template,request,flash,redirect,url_for
from .models import Post

blogb = Blueprint('blogb',__name__)


