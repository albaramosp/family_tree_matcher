Usage
=====

Registration
------------

To use Family Tree Matcher, first register. Use the model ``person.domain.model.Person``

.. autoclass:: person.domain.model.Person

This uses the function ``person.application.use_cases.SavePersonUseCase.save_person()``:

.. autofunction:: person.application.use_cases.SavePersonUseCase.save_person

Finding lost siblings
---------------------

To find possible siblings that match your newly created person Someone Example,
send a POST to /matcher/match_siblings/ with the following payload:

.. code-block:: json

   {
    "name": "someone",
    "surname": "example"
    }

Whenever some other person registers in the database, if it matches your data
you will be notified if it can be some member of your family!