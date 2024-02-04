# Family Tree Matcher
Find your lost ancestors with Family Tree Matcher!
This is a TDD and an attempt to learn more about architectures & design patterns.

## Parts in this project:
[![](https://mermaid.ink/img/pako:eNp9Ul1r2zAU_StCD0MBJ_ijSWw_DAZZ026UpfuAtXYpN9J1bLAlI8nd0pD_PjWOS1q66km699xzzj1oR7kSSFNa1OoPL0Fb8nORS-KO6dYbDW1JION1hdKau77xaXXZX1CKXL4CrzOhqwfUpFX6eeILa1EbJUdkPP5ISpCixnsDD0g-kN-sAG6V3o567FfWgOUl6hfgQ-3eVOu6khvjxm5ejb3lhWcgoLVO-ujjG1ud-LhmJ06ONCt2dar-nb2p_46myKBt64qDrZQ8yn5mvwwSDgaHyXO2UA1U0iONi79-jxD7QOWLQJfLYZPhvXw2_n-qIruUhQZjdcdtp_FIdnHBzvssPWLcejVa5ZwZC3aIRawzdqXkRo3uTuipRxvUbg_hPtDuqZFTW2KDOU3dVWABXW1zmsu9g0Jn1Y-t5DR1-ujRrhVOYFGBM9cMxRYkTXf0L03HQZREE9-fT-NZ5EfxWRB6dEvTwI8m8TyIpsk8Sma-n8z2Hn1UylGEkzAMQtecBmfxPE5mB77bQ--Jfv8PnAjuUQ?type=png)](https://mermaid.live/edit#pako:eNp9Ul1r2zAU_StCD0MBJ_ijSWw_DAZZ026UpfuAtXYpN9J1bLAlI8nd0pD_PjWOS1q66km699xzzj1oR7kSSFNa1OoPL0Fb8nORS-KO6dYbDW1JION1hdKau77xaXXZX1CKXL4CrzOhqwfUpFX6eeILa1EbJUdkPP5ISpCixnsDD0g-kN-sAG6V3o567FfWgOUl6hfgQ-3eVOu6khvjxm5ejb3lhWcgoLVO-ujjG1ud-LhmJ06ONCt2dar-nb2p_46myKBt64qDrZQ8yn5mvwwSDgaHyXO2UA1U0iONi79-jxD7QOWLQJfLYZPhvXw2_n-qIruUhQZjdcdtp_FIdnHBzvssPWLcejVa5ZwZC3aIRawzdqXkRo3uTuipRxvUbg_hPtDuqZFTW2KDOU3dVWABXW1zmsu9g0Jn1Y-t5DR1-ujRrhVOYFGBM9cMxRYkTXf0L03HQZREE9-fT-NZ5EfxWRB6dEvTwI8m8TyIpsk8Sma-n8z2Hn1UylGEkzAMQtecBmfxPE5mB77bQ--Jfv8PnAjuUQ)
## Patterns applied

| Pattern                |                                                          Description                                                          |
|------------------------|:-----------------------------------------------------------------------------------------------------------------------------:|
| Adapter                |                                                              xxx                                                              |
| Factory                |                      Abstract the creation of an object so that the caller doesn't need to know about it                      |
| Hexagonal architecture |                           Isolates the core logic of the application form the external dependencies                           |
| Singleton              |                    Instance an object only one time and return that instance any other times it is needed                     |
| State                  | Avoid if/else dependency when choosing an strategy by subclassing that behaviour and calling <br/>the sub-methods dynamically |

## Launch tests
To test with coverage, run the following commands:

    $ python -m unittest discover
    $ python -m coverage report