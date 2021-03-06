# -*- coding: utf-8 -*-
from django import forms

from ralph.lib.transitions.models import Action, Transition, TransitionModel


class TransitionForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        if not hasattr(self, '_transition_model_instance'):
            raise ValueError
        if not isinstance(self._transition_model_instance, TransitionModel):
            raise TypeError
        super().__init__(*args, **kwargs)
        model = self._transition_model_instance.content_type.model_class()
        field_name = self._transition_model_instance.field_name
        choices = tuple(model._meta.get_field(field_name).choices)
        self.fields['source'] = forms.MultipleChoiceField(choices=choices)
        self.fields['target'] = forms.ChoiceField(
            choices=(('', '-------'),) + choices
        )
        actions_choices = [
            (i.id, getattr(model, i.name).verbose_name)
            for i in Action.objects.filter(
                content_type=self._transition_model_instance.content_type
            )
        ]
        self.fields['actions'] = forms.MultipleChoiceField(
            choices=actions_choices, widget=forms.CheckboxSelectMultiple()
        )
        self.fields['actions'].required = False

    class Meta:
        model = Transition
        fields = ['name', 'source', 'target', 'actions']
