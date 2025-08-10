# from django.db import migrations


# def copy_address_and_letting(apps, schema_editor):
#     OldAddress = apps.get_model("oc_lettings_site", "Address")
#     OldLetting = apps.get_model("oc_lettings_site", "Letting")
#     NewAddress = apps.get_model("lettings", "Address")
#     NewLetting = apps.get_model("lettings", "Letting")

#     for old_address in OldAddress.objects.all():
#         new_address = NewAddress.objects.create(
#             number=old_address.number,
#             street=old_address.street,
#             city=old_address.city,
#             state=old_address.state,
#             zip_code=old_address.zip_code,
#             country_iso_code=old_address.country_iso_code,
#         )
#         old_address.new = new_address  # lien temporaire

#     for old_letting in OldLetting.objects.all():
#         # on retrouve la nouvelle adresse correspondante
#         address = NewAddress.objects.get(
#             number=old_letting.address.number, street=old_letting.address.street
#         )
#         NewLetting.objects.create(title=old_letting.title, address=address)


# class Migration(migrations.Migration):
#     dependencies = [
#         ("lettings", "0001_initial"),
#     ]

#     operations = [
#         migrations.RunPython(copy_address_and_letting),
#     ]



from django.db import migrations

def copy_address_and_letting(apps, schema_editor):
    # Si l'app d'origine n'est pas installée (DB neuve), on ne copie rien.
    try:
        OldAddress = apps.get_model("oc_lettings_site", "Address")
        OldLetting = apps.get_model("oc_lettings_site", "Letting")
    except LookupError:
        return

    NewAddress = apps.get_model("lettings", "Address")
    NewLetting = apps.get_model("lettings", "Letting")

    # On mappe les anciennes adresses vers les nouvelles pour relier les lettings proprement
    addr_map = {}
    for old in OldAddress.objects.all():
        new_addr = NewAddress.objects.create(
            number=old.number,
            street=old.street,
            city=old.city,
            state=old.state,
            zip_code=old.zip_code,
            country_iso_code=old.country_iso_code,
        )
        addr_map[old.pk] = new_addr

    for old_letting in OldLetting.objects.all():
        NewLetting.objects.create(
            title=old_letting.title,
            address=addr_map.get(old_letting.address_id),
        )

class Migration(migrations.Migration):
    dependencies = [
        ("lettings", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(copy_address_and_letting, migrations.RunPython.noop),
    ]
