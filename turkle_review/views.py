from django.contrib import admin
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import get_object_or_404, render

from turkle.models import Batch 

def process_batch_data(field_names, rows):
    # remove the MTurk-like metadata so we get input and answers
    keys = ['Turkle.Username']
    header = ['Username']
    for name in field_names:
        if name.startswith("Input."):
            keys.append(name)
            header.append(name[len("Input."):])
        elif name.startswith("Answer."):
            keys.append(name)
            header.append(name[len("Answer."):])
    rows = [[row[key] for key in keys] for row in rows]
    return header, rows

@staff_member_required
def review_batch_view(request, batch_id):
    batch = get_object_or_404(Batch, pk=batch_id)

    fieldnames, rows = batch._results_data(batch.task_set.all())
    fieldnames, rows = process_batch_data(fieldnames, rows)

    context = admin.site.each_context(request)
    context['title'] = f'Review for Batch: {batch.name}'
    context.update({
        'batch': batch,
        'field_names': fieldnames,
        'rows': rows,
    })

    return render(request, 'turkle_review/review.html', context)
