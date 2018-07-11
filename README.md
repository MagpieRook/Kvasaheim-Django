# Kvasaheim-Django
A Django rewrite of http://statistics.kvasaheim.com/.

## How to Install
First, install [Python 3.6.6](https://www.python.org/ftp/python/3.6.6/python-3.6.6.exe), which comes with [pip](https://pypi.org/project/pip/). Make sure your pip is updated by running `pip install --upgrade pip`

__Recommended:__ Using pip, install [virtualenv](https://virtualenv.pypa.io/en/stable/installation/).

Then, download Kvasaheim-Django.

### Using pipenv (Recommended for Heroku)
-- TODO --

### Using virtualenv (Recommended)
`virtualenv` is a tool to keep all of your code, packages, and dependencies in one place. To learn more about what a virtual environment is and why (and how) to use one, read [Python's documentation on venv](https://docs.python.org/3/tutorial/venv.html).

1. In the Kvasaheim-Django folder, use the command `virtualenv <foldername>`. It's recommended to use `.venv` or `.statsenv` as those are the names provided in the `.gitignore` file and hiding the virtual environment will clean the working directory.
2. Run the virtual environment:
    * **Windows:** `.venv\Scripts\activate.bat`
    * **Unix/Posix:** `source .venv\bin\activate`
    * [Full instructions on virtualenv.pypa.io](https://virtualenv.pypa.io/en/stable/userguide/#activate-script)

### Installing and Running Kvasaheim-Django
1. Run `pip install -r requirements.txt`. This will automatically fetch, download, and install the pip packages required to run Kvasaheim-Django.
2. Edit settings.py with DB information
3. `python manage.py migrate` and `python manage.py collectstatic`
4. `python manage.py runserver`
5. Login to site with google account
6. `python manage.py makesuperuser <google account username>`
7. Click the "Admin" link next to your username to access the `/admin` site.

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
