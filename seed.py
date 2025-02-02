from app import app
from models import db, Owner, Animal, Vet, AnimalVetVisit
from datetime import date

with app.app_context():
    # Delete existing records to reset the database (if necessary)
    db.drop_all()
    db.create_all()

    # Add sample Owners
    owner1 = Owner(
        name="John Doe", 
        address="123 Elm St", 
        phone_number="555-1234", 
        email="john@example.com"
    )
    owner2 = Owner(
        name="Jane Smith", 
        address="456 Oak St", 
        phone_number="555-5678", 
        email="jane@example.com"
    )

    # Add sample Vets
    vet1 = Vet(
        name="Dr. Alice", 
        specialty="Dermatology", 
        phone_number="555-1111", 
        email="alice@vetclinic.com"
    )
    vet2 = Vet(
        name="Dr. Bob", 
        specialty="Surgery", 
        phone_number="555-2222", 
        email="bob@vetclinic.com"
    )

    # Add sample Animals with long image URLs (replace with actual URLs)
    animal1 = Animal(
        name="Fluffy", 
        species="Cat", 
        animal_image="data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQABAAD/2wCEAAkGBwgHBgkIBwgKCgkLDRYPDQwMDRsUFRAWIB0iIiAdHx8kKDQsJCYxJx8fLT0tMTU3Ojo6Iys/RD84QzQ5OjcBCgoKDQwNGg8PGjclHyU3Nzc3Nzc3Nzc3Nzc3Nzc3Nzc3Nzc3Nzc3Nzc3Nzc3Nzc3Nzc3Nzc3Nzc3Nzc3Nzc3N//AABEIAKgAtAMBIgACEQEDEQH/xAAbAAACAwEBAQAAAAAAAAAAAAADBQIEBgABB//EADoQAAIBAwIDBQcDAwQBBQAAAAECAwAEERIhBTFBBhMiUWEycYGRobHwFCNCUsHxFTPR4WIHJIKisv/EABkBAAIDAQAAAAAAAAAAAAAAAAECAAMEBf/EACMRAAICAgEFAQADAAAAAAAAAAABAhEDIRIEEzFBUSIUIzL/2gAMAwEAAhEDEQA/ANYXMduxT2Su1ZCTUzufMmtDbzifhTuOarWX72RyVC53NWRAzreMyXIB6VeaPFCtYyniYYNTllbJxTgCxp4faxSbj8YEJIO9Xu8kbYVWv0LQkNzoeiGUt2fXTFWkAyKHboqyMDV1CMBRSBPLeSZ20rnJ5YGc1YaO5jbTMrqRzBGKZ9nbYtO7DwudlY/xH8iPXp8abcRtA8PdjJYZ0Hqp6Aeh5f4rLLq1HLwZrXSSli5mYUMN/vR4pWGRUkXUcH6UQxYrWZQPfHO9SWZetFEOa7ud6gCDOpGaBLpIzVowrjehvCumgEVzYBOKqytgU1NspbNBuLRWOKBBLJJgVSlk3p5cWA07UqubFtW1BhBrJsKNbtljUY7JtqN+kZTmgQnjO9dU44zoGa9okNvw+d4+FzKc4A60pN1kgU/lt3XhsmQoJXlWfhtW1dPhVkBGWBJIwwvKiRxsQS1Ft7TAy9WYo4vZprAVYljXOaq8RYd0+nlTeSBMbVSurYMpA8qATEd8yXe3U00gYhdR881Tvrfupz76sWr6iq9TsB50nhtsK+I2vBI1jghce0wJPxO/0AqzxJTGDoOCBz9arXRmsYou5Ge6UK3ywarXN886EKNB6noa4zjc3L6dvlWNL4VLtzFOQq+BhrHuyaCJ/TFMjHDcW6JNMkbIoCkkciM0C4sJIvGE1R9HXka6GDqYS0/Jzc2CUXa8FSS5xgVIT5GaGwycb/GolMDFarM1BO/ycV6Cp3POvbOwa4cM7rHF/UeZ9w6/m4p5BwyJU8EKN5mVdRI/tWfL1MMens0Yumnk34EwRSM0KWNc1f4nDHHG3dxLGUxkq3hYHP12pSdzzzTY8iyxtCZMcscuLJTRAjAqv+lXrRGOBioB2wcU7EBtbgHblQpIcDFGVznevJNR3HKgQrquBiuqRHnXtQJsrO0lkhA7xm26VVubaS3YK2cetWbS5nZQqeEVaVBKrJIcnzp06EaFyKAd+VWohFgVSuYmt3K/xro5NJ99OAY+AHahXCqy0FmYDIrxGLAk0SCDjloPaVcmvezPDJHn/WOP2rfx4zsWByByPp86dLa/rZlgGMk75pvxu6iseHx8Oto10jbK9T1rH1WXguKNHT4+Ttitu+mcSPHh5OY8qBHalrruJcZboaFas88VxccOuW7+NGk0NggkctiPrVN+L8b4XdRPxL9JIzR94bdEIfTkAlWHlncH4VgjjlLZtlkUdB7rABuJImEcMiq7EevSrkV1OtzKucRxuEhC7DccvXnQHdLuCK0TLQ3A1qRyKncGh3UMtoFk1lGLaVBGRuMcvjmhKGwxnoa8SuordotFnDJKTlscxUAtm6NcCAySdIyw0g+o/BVaGxRpoYrR8z6S8krnmOtdcSIkrxwsGdThmHI0j5J+WN+X6Llph5RJKMSNtpP8R0xR5LuOMsqvkrzpPJNPDCZYVMmDnSFJK1Rhuri8nK4IOSST099PLHcdFmOSTtlviMstwkkjP+2zBV+A/wC6WgYUCpXlyzuFif8AaTZTgb+tVMt/XXSwQ4Y0jmdRkWTI5ILIdqgjYBoTMc7nNRZvDVhSE170RZFxvVAu3SomUgYNAJfaRc11LxNXUCG0tLm59lY8J0NHaVw4JbeltvezSLsMelEw0m7yaKsFGs7xzIAxy450Du1UZqpFkuBEu/VqPexlVDFt6KZAy6dNcFVjjVilqy+E75qxw95JJViRyAxxgDP0ot6snuh5w6IWdtdXzNlY4ywG25HT886xn+pSNOZJphqY4OsbKD5b863Xa2UcM7KhWGGlOjEfPA3zXx2W4WWUrNIrajkEnfHTmP71zJ/2ZLNkFxgai0efh93HcBQ67oxVgQ6HoT0Ip9fXSyWzXEQtgZYu6eZtWoLjlpx/fBrLcDslmRnSZzgjwI2+fhkfOns8bG0dBGGIXJ04wPMnB3xSNuLofjGXkPwaJGgtP02ru4YRGmrnj1+VF4vHExlmvpe6traMys2flj1ruBXVh3CCC7WTmdRONRpbezPfXjxTKWiVyrofErqdsfL77UU6ewuGtFSGbiv6OC5th+jF6wjt4zCJGlJ6HfYaQTy6VeseKRSrNb8QhFrdRbOQvgY9NxyNMLW4h4ZbxW4uA8UJwivEWaP3HO/xpdxDjVuwK2too1vli4GqRjtkjHL40Z8WtiQ5J7COnewloZgE5ZRvT0NAkmSDhZYT6pBmMbY3O30G/wARS+BzHcOqgxhhnSOQJpnd2ivwYaATqnLZI6lV2zSYv9KLLpuotozushQDzoZkbO1XGszjcYPuoL2mN66dnNopuzFqOhJXehzRaQDUVfAIqWQ9LY2qDNtUO93r1pFxvzpQnma6o5Q711AJohG+vTqZVz0601tI4o42ZlJI86qXKPBK8UjaXRiD7qDHJ4iumrCsbLfpyjXerECd8C0xUZ6GkkcndzA4xmrCXbJIcdaISV5EsUjZkQA+QOftVvs3Akt7GAXKg6idOAcdM/PpVG8eWUHR0G5/p+PSmHCLlYle4OWZEC6saAfh1/NqryyqDLMauRPtdxQXtz3TgsijK4B8P/5H1rC3b2du/wC7DblicgdyJCc+gA+5p12mt73iEiyqsjYOy55euKUpOscbIcwyoMNNpGseinz9fKsOGdbNU16HfDOIpa2bx/o47YNg6dGlveVTf3ZNHa/DXBVGkBI8Qct8QQR/esM961hPpH8zsdWdI8/Vj5+VN7Zop1DKdiuG35Yq2XGTEi2ixacLt5b67ljl/wDarJmNYWx4uZ5Hlv8AatJbrDqCWoCbDwnfI8wevv8ApSKANA4e38Opd1zz+NX7Cd2EsfgRkXWNXL1yPL1+Wak4cvAym/ZHiJkddZALRnxKcH6Z+9KBfxSXIVo1jlHLQukH30ftHduSG0yEAfuIDh0xsWU+n8h8euRm2lkJVl21ey+cA+/yNJLHxJysc3M8q3jNp8JA38v+q+i9nrdZ+zsTzRKyuSRn02r5lC0l2FEo1EbZr7BNCttwe0jtwAqxKN/MCsuWVbRfjV+Sm3DbaUnwrUW4TaAZManNRt7rv+RIlXz60Rp2fbGGFVrKyxwRWm7PWcyHVGBnkRSuXsbE+dEmPSnX6iaM5PKrFvfhyNVWRzyXsSWJP0Zhew6aTql3oLdiFAOmbFbhpYyMrzqAdd8jB86fvy+idqPw+ev2KmDHTPtXVvDKAcA5rqn8mf0nYh8F3a3hAkK8UtlOH2kB6HkDWbW1RckyYAr6PLc2l5Yy23dE9/GcDGCxAzj189s9a+YZi7xvQ42rqRZzCUjQk+E5Pn+fCpBBguOVS0K0YKrmgyI4jOTgeVNYQ7O0wCgMcdAaZQM0dkEdV0Mxwrkjf12+lK7JdXhRDIw55Jxj5Ux4gVmshbp4Zk8QC5/5NZOplUaNHTq5WVblJpY/3HXUDsUbGD6VluLQR3VwVDkPGM886z5n1qxb389vetDcu64BBJol/HBKupHMbYznqffWKNpmp7Rkpta/767nrU7e8msyTG21FvldZNsOASSAedUxGHBYalz5Lt8RWlFDHA7QXBB0kDC8wN68tOIXcd1FcNKSI3VzvzXqp94yKTLHkEZzjrQ++KEqFyOtMruwNm1WMR61eY6YZdBbqp5RyfLKHpgLUHhhiRwIkRW3dMf7Tdcen51FLo5ZbniQiVSIrmNEchSdmVd//iw1U4tOB3cumS8cKzL3cyA88bdPT82qZZL2x4p+itZSEXCRjDOOeOlfSreeSTgcZkcllOkAjpisvYcMsrJlCq0rKAAwStLblpbJv/E+yy8qwT2aY6FzllLSscBTUpboECWM5I50tupC9yVIA26cqnCQgMTDGobGqqLLGsF2s0ef5VxmwM0oijeF9Wv3VbNyrxkKuWHNqlEsY2V0pYgp8aJPcaGUo3M70s7wCHWnPrRI5e8izhR6miAb9+h3059a6li6QN5flXU1Esb2DRWUluzSd8UGnI3QgdSd87jzPOsj2hSKHi1x3eMs5kGOW9aWFf1NorCNVCIoZ2OSfTbng7j2s+maQdsrUpJZT5YytHpYnmcdTXbOMJxfgIUGMjyrx7gtueZpeI9JKO2jPIjrXPIV2JzimIXonPeB1bB9+1e3d7cJc96gcgL4iOVLkuCHVFVX1nBDE7evOm93G2QrIe7AGABkk4rJ1FGjB4KUsNnxUd5q7uQbAjGCfWl9xw+/tyFjIlU+W2wos+qM6YgApOAU5/GvUvJhpEjsD7PocH8+lZdmgRzSz95+9Fvk5O43/BVfXG6kKcEdP7itTNOkqoN+fiLYwOW4+nzpHeWlnKW7pCgDblTuPTHlVkZL2K0JZpPEApJblkCrdnw2TvNUgU4323Cjnmj2tksZJUB31cifpV+RtICIrDUcYUbsfIenr8KeU/SFURnZTwwKmP4qMbbk9Dj41p7UNdoZHUqjgPgjr126dayEIS1UFgWmcAhscvcB5U+sZZ7lEabu4UGQoOct7gPX0JrNMviaKEICB4dXqM0+sYtVsx2+AIrM2tvyaZp2zvpyqj75+taPgmhW04ZATuGbP96qQ70ZDtBmC6RlzkMeea8XXJbqTzNMe2PD9M6Pgc84Ubml0IJRNL7+VSSCj2aFgoAKhuhOagjaMxkh2PMirTrI2zcqrTaYCSVzmpQGw1u22lyTjz5VMOplBXGnrilxuwGAUZJ6YzipzTNGusBnI6AYxUUSWXWmlViFC49a6k/6osSWUgnzrymolmptOIRQCR7iWPvlGdCjkM55Ecsg8wMYO+wql2lP6vhjTRkCRWUpvvp5fYVn4eKW8LbaZQhJXUMKRgYIHwOcEHwepo0fFJbmLXIQpwWKgbDJJ+9dl+TkiiRWDgygnA2JFLry5XBycb8qPxHiMly/dQMJJDsMdKt8E7LXNzcJJckZ6gjI+VQgw7J2VtdB7uaIgQjXk/xI5evltyq1eqJdUgjnI/rUGtSvCbbhlkkEEIJmPiIUcv8ANAmjkx+1OVb+kAVzc8/3Ruwx/Bh5WYDDO7q3IAb/ACpZLJGsemRWctnDL+cq1XGrWGeRYv8AavGXKSKMK58iPw1m7hO7bu7qMxyruxHI+tCGxpFNJm7s9y5YAaSDuBXrlNPgYhsDOBkCgSQiASAeHUOjYyOldauGXEmMsdwdsfhqyhLCRyGN2EEet25grn0+Q/5ryO5CXZUfuSxLufXqT7vKiC4MUTMrBi6sEI5AfnWg2yxwyS6ecsnjH/gOQ896KWiN7HXC7ZmlSWTBkdspq5KNt/cP+K1kCpApY6Q4/k25HwrPWEpgVpWbBI38OdIr2zln4vdtF3ndQnYnB3HpWafkuiNJuMM8ndWpYv5YJ+1NeDS8XSdWeFivU6cVZ4TZW9pEI7aJdQ2LY5n30/ghfRv3X1zVT8ll6AcbVrqw1vGRt4gTWS/TyI+oAEeQ6V9Ba3aa1aJoxy8LbkZrH3cUkEjpKFJIyQQBjf507iJGQGMt/MqffQrnQygax7gv/VQlmjQnLrihtciSEiIAgdRRihpMp3EGZfabT/QBjNAVxCNEbjJ9pS3KiXkmtdCKfXPKl5nXuiqkBh0ApuJXZd/T2h3aJST11c66qad4VBMu/lnFdR4gsRM0MRkkmk3bJZc7EnBO/Xr86v8ACYLviiFYv27crpG+PjUOD/8Ap9xHiJWXiEmhBzGeXptyr6Bwvs7Bw2HRbQ9R4iCNXz+9dVI5zYq4RwGz4ahKKZZf6zyNavg1oJc6NI07ux5AUbhlgt1MDPJKLcbs2NvdROLcVs7SN7e0jITqwO5qrNlUFXssxY+bKvELkSTYBJRdhmk15eaQREM45+lRk4jE76UBGOYPOoXJix3iMBq2Oa5b/Ujor8oR8Qik4qXjgGXiAMZz165qlC0tx31tcwCRottxnGPLG9RkuJYr6RbNsyM+lFUbGrPCrb9Bes00/eSH2ghB8WeXvq1RlaorclRkuIlYJWBJOg40H89edVRKHQlTk861faDszd8WvO/4cpiYkBzIdm3225g9KWQ9heLHV3k9sp6bkk/TyrasToyvIrEjXWG0t15fnwFeQz5uh68/hTluxPFmXU00K52ByxJ5nGw91V5uxvF7cGQPE56KrHJ+B930NMsToXuIt3F6vdLFEAwbdgd60vZuIIoKlTJJt4eX5isXb8L4pAwVrOdipOcJnlz+xrZdmVZLYTyl107YccjWbLjouxzs20LCNQBjA8udW4nlkGUYhfWqMTBkUgkkjkOVMuHOykHQfXNYJL9GxeDQ8OdGtANYLbnFYntXayxcTkkRwuoZwcf3rXv4oGkiwMc8fekl8kV/IJJ4HYIN3V8cunP8JHnWzHjctGWc+GzA3L6NTXKyyj+lUJzVCK+vyStpwa5CnkTyr6Za2AlGmOCMoh3UPn3b/nMeVc8SaJpEt2/aIB29rOw+4+Z8q1R6aKRRLPJs+cQ2nGbzWJLYd4MBhkAb1IcK4wyBHsSSu2Bjfl1+NfQ0RwQ8dqE7w6/HjYnG/wBvkas3MOZI1WNMgeE53XPX6/8A1o/x4g70j58nArqVFYQ6Nt1aQAiurfwcM75Mm3TAJxlt/P6Zx8K9qdiIO7IsCNQrJCCFGFxpbb3b/b50UW8bYB05HPbAI+/w5UZRLKD4Qq6uQ+9F04yN9R+fxqwrEHaXif8ApkUShgEkOkaBjpyrMTcSiuLR2LA7HVjpT7tRwObiS93K57gbgRnGD5msiexbxSFYrqdAwwSWG9Vzw83ZbDLwQOwukW5ZiQQU8JPPAofEr7vAtnw4NPNL7WnkopxZ9k7KziZZHkmZuRdthVu04VDayFbKLSGHlUh00U7YZdQ2qQp4Twe1s1WRYi9wcgvKudB91M04e1wxklJUbBnbGdXp9NuVM47KFAWlkwTjbUelTlDXkipGWVccgTWqo+ii2UXTQpS3jCeHfBGTjr6VEWak948LNkagGwTnffcep/DV1oYE2LNq9n2jUorSNwDcEhRsSTnIqCipoe+/cmUl/wCBVFwpz/j8NENnoB0xsWPskryPy934aZyONXdxRsVGwIFFijKnxMWJ8+lQhTjtv0yowiUOeWlcn/obUoveDvBO06OApcaosYAHof7VrHRY1RvadeTeWaUccikktXMcjHSM4FVzjyTHi+LQWO4iSIHw7CpWfF0aQoGAx5VjP9Zt8aQ5BGxBotvxO23aN8v0rlvC7OgsiPqPCb6KSOSNjnI51K3s41RljbvFLZO+4r57w3jsO2ZMOWxWo7P3E6XTpqLK+4zyrRh5LRTlpmjChItKxafIfn5uaqSWuqIqRlX5jJ+X55mr+tgMMg+FDLM7YQYUVrsylBLcYDzL7RyRqO35n60TSvdSSyHJJzq35eX3+dWZCByoDmR9kVSo9rNEgHwKAPT/AD9c17Xvj/p+VdUIEDM4Ko2B1o2gKgAOTXV1IQBKqkb6tXXFLri3LEsM59a6upkQqGJywLcutGCRAERjB866upwFZomZ/Ec+tGIMQ0xjBPM11dRATgtkQd5K2Selc+GJIGBXtdUIQ5UWEqoyVzXV1Qh42l/FpoTwmTwqpw3PPKvK6oQgOzPDgTJLaxySt1xXL2M4VEhEVsmp9ziva6gwosW/ZKwt3VhAqmm8VhFBIpj5eldXUoQx1Z8LY86kp09c5rq6gQ8lC4GaqzkBiFbBryuqEPI0LLknJryurqBD/9k=",  # Replace with the long URL
        age=5, 
        owner=owner1
    )
    animal2 = Animal(
        name="Rex", 
        species="Dog", 
        animal_image="data:image/webp;base64,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",  # Replace with the long URL
        age=3, 
        owner=owner2
    )

    # Add Vet Visits
    visit1 = AnimalVetVisit(
        animal=animal1, 
        vet=vet1, 
        visit_date=date(2025, 1, 1), 
        notes="Routine check-up"
    )
    visit2 = AnimalVetVisit(
        animal=animal2, 
        vet=vet2, 
        visit_date=date(2025, 1, 1), 
        notes="Surgical consultation"
    )

    # Commit all to the database
    db.session.add_all([owner1, owner2, vet1, vet2, animal1, animal2, visit1, visit2])
    db.session.commit()

    print("Database seeded successfully!")
