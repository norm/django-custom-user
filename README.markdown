django-custom-user
==================

A Django 1.9 application with a more sensible `User` model. Used as the base
of new projects. The `User` model provides:

*   email address instead of "username" as the primary field
    
    Signing up with your email address is a much more common pattern.

*   ("Full Name", "Familiar Name") instead of ("First Name", "Last Name")

    Names are more complex than first/last. Instead of trying to force users
    to approximate their name in a split form field, ask for it in full and
    allow them to provide a familiar name if you want to use `get_short_name`.

    For example, my name is "Mark Norman Francis", but I like to be addressed
    as "Norm". There is no way the first/last pattern can capture this.

    As the [UK Government Service Design Manual says][sdm]: "Be sensitive to
    different cultural conventions when asking for people’s names. If you can,
    use a single name field."

[sdm]: https://www.gov.uk/service-manual/user-centred-design/resources/patterns/names.html
