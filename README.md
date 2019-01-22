# Kvasaheim-Django
A Django rewrite of http://statistics.kvasaheim.com/.

## How to Install
First, install [Python 3.7](https://www.python.org/downloads/release/python-370/), which comes with [pip](https://pypi.org/project/pip/). Make sure your pip is updated by running `pip install --upgrade pip`.

Then, download or clone Kvasaheim-Django.

### Using pipenv (Recommended)
Using pip, install [pipenv](https://docs.pipenv.org/) with the command `pip install --user pipenv`. The `--user` flag is used "to prevent breaking any system-wide packages", [as explained here](https://docs.pipenv.org/install/#installing-pipenv).

`pipenv` is a package manage similar to npm in Node.js or bundler in Ruby. It uses Pipfile and Pipfile.lock files rather than the requirements.txt file, which is automatically updated when you use pipenv to install any packages. It also, as the name suggests, takes care of keeping track of your virtual environment for you.

1. In the Kvasaheim-Django folder, use the command `pipenv install`. This will look at the supplied Pipfile and Pipfile.lock and install all packages and dependencies listed.
2. Run the virtual environment with the command `pipenv shell`. You can also run commands in pipenv without opening the shell with `pipenv run [command]`. For example: `pipenv run python manage.py runserver`.

### Using virtualenv
Using pip, install [virtualenv](https://virtualenv.pypa.io/en/stable/installation/) with the command `pip install virtualenv`.

`virtualenv` is a tool to keep all of your code, packages, and dependencies in one place. To learn more about what a virtual environment is and why (and how) to use one, read [Python's documentation on venv](https://docs.python.org/3/tutorial/venv.html).

1. In the Kvasaheim-Django folder, use the command `virtualenv <foldername>`. It's recommended to use `.venv` or `.statsenv` as those are the names provided in the `.gitignore` file and hiding the virtual environment will clean the working directory.
2. Run the virtual environment:
    * **Windows:** `.venv\Scripts\activate.bat`
    * **Unix/Posix:** `source .venv\bin\activate`
    * [Full instructions on virtualenv.pypa.io](https://virtualenv.pypa.io/en/stable/userguide/#activate-script)
3. Run `pip install -r requirements.txt`. This will automatically fetch, download, and install the pip packages required to run Kvasaheim-Django.

### Installing and Running Kvasaheim-Django
1. Install Kvasaheim-Django using one of the methods above, or using pip directly.
2. Edit `stats/settings.py`. Update the following variables:
    * `SECRET_KEY`.
    * `DEBUG` is by default `False` and uses an environment variable.
    * `DATABASES`.
    * `AUTHENTICATION_BACKENDS` uses [Social App Django](https://github.com/python-social-auth/social-app-django) with Google authentication by default. You can [restore password authentication](https://docs.djangoproject.com/en/2.0/topics/auth/customizing/#specifying-authentication-backends) or set up [more social backends](http://python-social-auth.readthedocs.io/en/latest/configuration/django.html#authentication-backends). If you keep Google OAuth2, see __Settings for Google Authentication__. If you add more authentication methods, including restoring password authentication, see __Adding Authentication Methods__.
    * Change Internationlization variables as necessary, especially `TIME_ZONE`.
3. Run `python manage.py migrate` to set up the initial database state and `python manage.py collectstatic` to set up static files.
4. Run the server with `python manage.py runserver`.
5. Login to site using the link in the top right.
6. Once your account has been authenticated, run the command `python manage.py makesuperuser <account username>`. For example, for the account kvasaheim@example.com: `python manage.py makesuperuser kvasaheim`. 
7. Click the "Admin" link next to your username to access the `/admin` site.

### Settings for Google Authentication
As mentioned above, Kvasaheim-Django uses Google OAuth2 through Social App Django. To set up Google OAuth2, you will need a Google account set up as an admin.
1. Start a project at the [Google Cloud Platform](https://console.cloud.google.com/). Give it a project name, ID, and optionally select a folder in which your project will live.
2. Go to your new project's [APIs & Services](https://console.cloud.google.com/apis/dashboard) page, specifically the [Credentials section](https://console.cloud.google.com/apis/credentials).
3. Select `Create credentials` and `OAuth client ID`. If the `Configure consent screen` warning appears, follow the directions until you return to the `Create OAuth client ID` screen.
4. Select `Web applciation`. Enter a name, for example `Kvasaheim Django`.
6. Under Authorized redirect URIs, fill in `[example.com]/account/complete/google-oauth2/`. Instead of example.com, fill in the base URL for your project or `localhost:8000` (or a customized local URL) if running locally. Note: You can add multiple lines here, prefixed by `http[s]://` to be recognized.
7. After you click `Create` your Client ID and Client secret will appear. In `settings.py` fill in `SOCIAL_AUTH_GOOGLE_OAUTH2_KEY` with your full Client ID and `SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET` with your full secret key.
8. Replace `example.com` in `SOCIAL_AUTH_GOOGLE_OAUTH2_WHITELISTED_DOMAINS`. This variable is used to whitelist certain domains, which will be the only domains allowed to access your site through Google Authentication. You can comment out or remove this variable, or set to a blank list, to remove this functionality. If using this variable, remember to consider whitelisting `gmail.com` to allow most Google users to access your site.

### Adding Authentication Methods
By default, the only authentication method is through Google. If adding password authentication or more authentication methods through [Social Auth](http://python-social-auth.readthedocs.io/en/latest/index.html), you will need to edit a few files in Kvasaheim-Django.
1. In `stats/urls.py`, uncomment the `login` url.
2. In `kvasaheim/templates/kvasaheim/base.html`, replace `<li class="nav-item"><a href="{% url 'social:begin' 'google-oauth2' %}">Login</a></li>` with `<li class="nav-item"><a href="{% url 'login' %}">Login</a></li>`.
3. In `kvasaheim/templates/registration/login.html`, you'll need to add forms for any authentication methods. Provided are a sample Google authentication link and a commented Username and Password form.

## Problem Documentation
In its current form, the Problem has a few intricacies that need to be addressed.
1. "Text" is a field that takes the body text of the problem, describing what the problem is. It is labeled as [safe](https://docs.djangoproject.com/en/2.0/ref/templates/builtins/#std:templatefilter-safe) and therefore will not autoescape HTML.
2. "Equation" is a field that takes Python code. It's required to include a `solve(x)` function that takes the input of the Problem's instances, does something to it, and returns the correct answer. You may write more code than this as long as it's valid Python code that can be run on the server.
3. "Random low" and "Random high" are the upper and lower bounds of the `randint` function, inclusive. "Num rands low" and "Num rands high" are the same, but for the number of random numbers generated. This allows for, for example, between 5-10 numbers between 10-100, resulting in a list of `41, 98, 76, 21, 66` or `55, 23, 70, 27, 92, 46, 26, 99`.
4. Formula, Solution, Rcode, and Excel are sections from [Project Scarlet](http://statistics.kvasaheim.com/samplestatistics/mean.php). These are also marked `safe` by our templates, accept valid HTML, and are written as to accept MathJax, as well. There are a few notes here for inserting the values of a sample, however.
  * @list will insert the comma-separated list of numbers.
  * @length will insert the length of the list of numbers for the problem instance.
  * @length1 will insert the length+1, commonly used in Excel code (`A2:A6` for a sample of 5, for example).
  * @addition will insert the list of numbers joined by `+` signs: `1+2+3+4+5`.
  * @multiplication, @division, @subtraction will do the same.
  * @breaks will insert the list of numbers joined by `<br>`, breaking it into a vertical list.
  * @sum will insert the sum of the list.
  * @answer will insert the answer to the problem instance.
