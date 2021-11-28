from abc import ABC
from django.forms.models import ALL_FIELDS
from django.shortcuts import get_object_or_404, redirect, render
from .forms import MoveForm
from .models import Equipement
from .models import Animal


def post_list(request):
    equipements = Equipement.objects.all()
    animals = Animal.objects.all()
    return render(request, 'animalerie/post_list.html', {"animals": animals, "équimements":equipements})

def aller_mangeoire(animal, ancien_lieu, nouveau_lieu):
    if animal.etat == "affamé":
        if nouveau_lieu.disponibilite == "libre":
            ancien_lieu.disponibilite = "libre"
            nouveau_lieu.disponibilite = "occupé"
            animal.etat = "repus"
            ancien_lieu.save()
            nouveau_lieu.save()
            animal.save()
            print(f"{animal.id_animal} occupe maintenant : ", nouveau_lieu)
            return 1
        else:
            print(f"désolé, {nouveau_lieu} n'est pas libre")
            return 0
    else:
        print(f"désolé, {animal.id_animal} n'a pas faim")
        return -1

def aller_nid(animal, ancien_lieu, nouveau_lieu):
    if animal.etat == "fatigué":
        if nouveau_lieu.disponibilite == "libre":
            ancien_lieu.disponibilite = "libre"
            nouveau_lieu.disponibilite = "occupé"
            animal.etat = "endormi"
            ancien_lieu.save()
            nouveau_lieu.save()
            animal.save()
            print(f"{animal.id_animal} occupe maintenant : ", nouveau_lieu)
            return 1
        else:
            print(f"désolé, {nouveau_lieu} n'est pas libre")
            return 0
    else:
        print(f"désolé, {animal.id_animal} n'est pas fatigué")
        return -1

def aller_litière(animal, ancien_lieu, nouveau_lieu):
    if animal.etat == "endormi":
        if nouveau_lieu.disponibilite == "libre":
            ancien_lieu.disponibilite = "libre"
            animal.etat = "affamé"
            ancien_lieu.save()
            nouveau_lieu.save()
            animal.save()
            print(f"{animal.id_animal} occupe maintenant : ", nouveau_lieu)
            return 1
        else:
            print(f"désolé, {nouveau_lieu} n'est pas libre")
            return 0
    else:
        print(f"désolé, {animal.id_animal} n'est pas endormi")
        return -1

def aller_roue(animal, ancien_lieu, nouveau_lieu):
    if animal.etat == "repus":
        if nouveau_lieu.disponibilite == "libre":
            ancien_lieu.disponibilite = "libre"
            nouveau_lieu.disponibilite = "occupé"
            animal.etat = "fatigué"
            ancien_lieu.save()
            nouveau_lieu.save()
            animal.save()
            print(f"{animal.id_animal} occupe maintenant : ", nouveau_lieu)
            return 1
        else:
            print(f"désolé, {nouveau_lieu} n'est pas libre")
            return 0
    else:
        print(f"désolé, {animal.id_animal} n'est pas en état de faire du sport")
        return -1



def animal_detail(request, id_animal):
    animal = get_object_or_404(Animal, id_animal=id_animal)
    ancien_lieu = get_object_or_404(Equipement, id_equip=animal.lieu.id_equip)
    if request.method == "POST":
        form = MoveForm(request.POST, instance=animal)
    else:
        form = MoveForm()
    if form.is_valid():
        nouveau_lieu = get_object_or_404(Equipement, id_equip=animal.lieu.id_equip)

        if nouveau_lieu.id_equip == "mangeoire":
            id = aller_mangeoire(animal,ancien_lieu, nouveau_lieu)
        if nouveau_lieu.id_equip == "roue":
            id = aller_roue(animal,ancien_lieu, nouveau_lieu)
        if nouveau_lieu.id_equip == "nid":
            id = aller_nid(animal,ancien_lieu, nouveau_lieu)
        if nouveau_lieu.id_equip == "litière":
            id = aller_litière(animal,ancien_lieu, nouveau_lieu)

        if id == 1:
            form.save()
        return redirect('animal_detail', id_animal=id_animal)
    else:
        lieu = get_object_or_404(Equipement, id_equip=animal.lieu.id_equip)
        form = MoveForm()
        return render(request,
                  'animalerie/animal_detail.html',
                  {'animal': animal, 'lieu': lieu, 'form': form})