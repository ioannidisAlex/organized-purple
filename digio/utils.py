# a try for creating a view

import logging

from django.db import migrations
from django.apps import apps


class CreateView(migrations.CreateModel):
    def _create_standard_view(self, model, schema_editor):
        sql_template = 'CREATE VIEW %(table)s AS %(definition)s'
        qs = str(model.view())
        args = {
            'table': schema_editor.quote_name(model._meta.db_table),
            'definition': qs,
        }
        sql = sql_template % args
        self._create_view_from_raw_sql(sql, schema_editor)

    def _create_view_from_raw_sql(self, sql, schema_editor):
        schema_editor.execute(sql, None)