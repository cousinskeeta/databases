from flask import flash

def new_user_test(request, db, Users):
    # Checking for empty fields
    if not request.form['username']:
        flash('Please enter Username')
    elif not request.form['email']:
        flash('Please enter Email')
    # Checking if passwords match
    elif not request.form['password'] == request.form['password_verify']:
        flash('Passwords do not match')
    ## Query database vs request to see if username taken
    try: 
        r = db.session.query(Users).filter(Users.username == request.form['username']).all()
        found = [i.username for i in r][0]
        flash(f"The username:'{found}'; is already taken")
    except:
        pass

    ## Query database vs request to see if email already registered
    try: 
        r = db.session.query(Users).filter(Users.email == request.form['email']).all()
        found = [i.email for i in r][0]
        print(found)
        flash(f"'{found}' \n This email is already registered")
    except:
        pass
