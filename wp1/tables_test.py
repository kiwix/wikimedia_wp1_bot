import unittest
from unittest.mock import patch

import attr

from lucky import tables
from lucky.base_db_test import BaseWpOneDbTest
from lucky.constants import AssessmentKind, CATEGORY_NS_INT, GLOBAL_TIMESTAMP_WIKI, TS_FORMAT
from lucky.models.wp10.category import Category
from lucky.models.wp10.rating import Rating

class TablesCategoryTest(unittest.TestCase):
  GLOBAL_SORT_QUAL = {
    b'FA-Class':     500,
    b'FL-Class':     480,
    b'A-Class':      425, 
    b'GA-Class':     400,
    b'B-Class':      300,
    b'C-Class':      225, 
    b'Start-Class':  150,
    b'Stub-Class':   100,
    b'List-Class':    80, 
    tables.ASSESSED_CLASS:   20,
    tables.NOT_A_CLASS:      11,
    b'Unknown-Class': 10,
    tables.UNASSESSED_CLASS:  0,
  }

  GLOBAL_SORT_IMP = {
    b'Top-Class':    400,
    b'High-Class':   300, 
    b'Mid-Class':    200,
    b'Low-Class':    100, 
    tables.NOT_A_CLASS:      11,
    b'Unknown-Class': 10,
    tables.UNASSESSED_CLASS:  0,
  }

  def test_commas(self):
    actual = tables.commas(1200300)
    self.assertEqual('1,200,300', actual)

  def test_commas_small_number(self):
    actual = tables.commas(123)
    self.assertEqual('123', actual)

  def test_labels_for_classes(self):
    actual_qual, actual_imp = tables.labels_for_classes(
      self.GLOBAL_SORT_QUAL, self.GLOBAL_SORT_IMP)

    self.assertEqual(len(self.GLOBAL_SORT_QUAL), len(actual_qual))
    self.assertEqual(len(self.GLOBAL_SORT_IMP), len(actual_imp))

    for k, actual in actual_qual.items():
      if k == tables.ASSESSED_CLASS:
        expected = '{{Assessed-Class}}'
      else:
        expected = '{{%s}}' % k.decode('utf-8')
      self.assertEqual(expected, actual)

    for k, actual in actual_imp.items():
      if k == tables.UNASSESSED_CLASS:
        expected = 'No-Class'
      else:
        expected = '{{%s}}' % k.decode('utf-8')
      self.assertEqual(expected, actual)

  def test_get_global_categories(self):
    actual = tables.get_global_categories()

    self.assertEqual(4, len(actual))
    self.assertTrue('sort_imp' in actual)
    self.assertTrue('sort_qual' in actual)
    self.assertTrue('qual_labels' in actual)
    self.assertTrue('imp_labels' in actual)

    self.assertEqual(self.GLOBAL_SORT_IMP, actual['sort_imp'])
    self.assertEqual(self.GLOBAL_SORT_QUAL, actual['sort_qual'])

class TablesDbTest(BaseWpOneDbTest):
  global_articles = [
    (225, 100, 475),
    (150, 0, 625),
    (100, 100, 229),
    (150, 100, 589),
    (150, 200, 596),
    (150, 100, 398),
    (0, 0, 109),
    (225, 100, 434),
    (150, 300, 629),
    (150, 300, 629),
    (150, 300, 629),
    (100, 100, 461),
    (225, 0, 288),
    (0, 0, 35),
    (150, 100, 665),
    (150, 100, 527),
    (100,0, 176),
    (150, 100, 37),
    (15, 100, 279),
    (150, 100, 279),
    (100, 100, 415),
  ]

  ratings = [
    (b'Art of testing', b'FA-Class', b'Top-Class'),
    (b'Testing mechanics', b'FA-Class', b'Top-Class'),
    (b'Rules of testing', b'FA-Class', b'Top-Class'),
    (b'Test practices', b'FL-Class', b'Top-Class'),
    (b'Testing history', b'FL-Class', b'High-Class'),
    (b'Test frameworks', b'FL-Class', b'High-Class'),
    (b'Testing figures', b'A-Class', b'High-Class'),
    (b'Important tests', b'A-Class', b'High-Class'),
    (b'Test results', b'A-Class', b'Mid-Class'),
    (b'Test main inheritance', b'GA-Class', b'Mid-Class'),
    (b'Test sub inheritance', b'GA-Class', b'Mid-Class'),
    (b'Test other inheritance', b'GA-Class', b'Mid-Class'),
    (b'Testing best practices', b'B-Class', b'Low-Class'),
    (b'Testing tools', b'B-Class', b'Low-Class'),
    (b'Operation of tests', b'B-Class', b'Low-Class'),
    (b'Lesser-known tests', b'C-Class', b'Low-Class'),
    (b'Failures of tests', b'C-Class', b'Low-Class'),
    (b'How to test', b'C-Class', b'Low-Class')
  ]

  project_categories = [
      {'c_category': b'High-importance_Catholicism_articles',
       'c_ranking': 300,
       'c_rating': b'High-Class',
       'c_type': b'importance'},
       {'c_category': b'Low-importance_Catholicism_articles',
        'c_ranking': 100,
        'c_rating': b'Low-Class',
        'c_type': b'importance'},
       {'c_category': b'Mid-importance_Catholicism_articles',
        'c_ranking': 200,
        'c_rating': b'Mid-Class',
        'c_type': b'importance'},
       {'c_category': b'NA-importance_Catholicism_articles',
        'c_ranking': 25,
        'c_rating': b'NA-Class',
        'c_type': b'importance'},
       {'c_category': b'',
        'c_ranking': 21,
        'c_rating': b'NotA-Class',
        'c_type': b'importance'},
       {'c_category': b'Top-importance_Catholicism_articles',
        'c_ranking': 400,
        'c_rating': b'Top-Class',
        'c_type': b'importance'},
       {'c_category': b'Unknown-importance_Catholicism_articles',
        'c_ranking': 0,
        'c_rating': b'Unknown-Class',
        'c_type': b'importance'},
       {'c_category': b'A-Class_Catholicism_articles',
        'c_ranking': 425,
        'c_rating': b'A-Class',
        'c_type': b'quality'},
       {'c_category': b'B-Class_Catholicism_articles',
        'c_ranking': 300,
        'c_rating': b'B-Class',
        'c_type': b'quality'},
       {'c_category': b'Book-Class_Catholicism_articles',
        'c_ranking': 55,
        'c_rating': b'Book-Class',
        'c_type': b'quality'},
       {'c_category': b'C-Class_Catholicism_articles',
        'c_ranking': 225,
        'c_rating': b'C-Class',
        'c_type': b'quality'},
       {'c_category': b'Category-Class_Catholicism_articles',
        'c_ranking': 50,
        'c_rating': b'Category-Class',
        'c_type': b'quality'},
       {'c_category': b'Disambig-Class_Catholicism_articles',
        'c_ranking': 48,
        'c_rating': b'Disambig-Class',
        'c_type': b'quality'},
       {'c_category': b'FA-Class_Catholicism_articles',
        'c_ranking': 500,
        'c_rating': b'FA-Class',
        'c_type': b'quality'},
       {'c_category': b'FL-Class_Catholicism_articles',
        'c_ranking': 480,
        'c_rating': b'FL-Class',
        'c_type': b'quality'},
       {'c_category': b'FM-Class_Catholicism_articles',
        'c_ranking': 460,
        'c_rating': b'FM-Class',
        'c_type': b'quality'},
       {'c_category': b'File-Class_Catholicism_articles',
        'c_ranking': 46,
        'c_rating': b'File-Class',
        'c_type': b'quality'},
       {'c_category': b'GA-Class_Catholicism_articles',
        'c_ranking': 400,
        'c_rating': b'GA-Class',
        'c_type': b'quality'},
       {'c_category': b'Category:Image-Class Catholicism articles',
        'c_ranking': 47,
        'c_rating': b'Image-Class',
        'c_type': b'quality'},
       {'c_category': b'List-Class_Catholicism_articles',
        'c_ranking': 80,
        'c_rating': b'List-Class',
        'c_type': b'quality'},
       {'c_category': b'NA-Class_Catholicism_articles',
        'c_ranking': 25,
        'c_rating': b'NA-Class',
        'c_type': b'quality'},
       {'c_category': b'',
        'c_ranking': 21,
        'c_rating': b'NotA-Class',
        'c_type': b'quality'},
       {'c_category': b'Portal-Class_Catholicism_articles',
        'c_ranking': 45,
        'c_rating': b'Portal-Class',
        'c_type': b'quality'},
       {'c_category': b'Project-Class_Catholicism_articles',
        'c_ranking': 44,
        'c_rating': b'Project-Class',
        'c_type': b'quality'},
       {'c_category': b'Redirect-Class_Catholicism_articles',
        'c_ranking': 43,
        'c_rating': b'Redirect-Class',
        'c_type': b'quality'},
       {'c_category': b'Start-Class_Catholicism_articles',
        'c_ranking': 150,
        'c_rating': b'Start-Class',
        'c_type': b'quality'},
       {'c_category': b'Stub-Class_Catholicism_articles',
        'c_ranking': 100,
        'c_rating': b'Stub-Class',
        'c_type': b'quality'},
       {'c_category': b'Template-Class_Catholicism_articles',
        'c_ranking': 40,
        'c_rating': b'Template-Class',
        'c_type': b'quality'},
       {'c_category': b'Unassessed_Catholicism_articles',
        'c_ranking': 0,
        'c_rating': b'Unassessed-Class',
        'c_type': b'quality'},
    ]

  stats = [
    {'n': 2, 'q': b'C-Class', 'i': b'Low-Class'},
    {'n': 1, 'q': b'C-Class', 'i': b'Unknown-Class'},
    {'n': 3, 'q': b'Start-Class', 'i': b'High-Class'},
    {'n': 6, 'q': b'Start-Class', 'i': b'Low-Class'},
      {'n': 1, 'q': b'Start-Class', 'i': b'Mid-Class'},
    {'n': 1, 'q': b'Start-Class', 'i': b'Unknown-Class'},
    {'n': 3, 'q': b'Stub-Class', 'i': b'Low-Class'},
    {'n': 1, 'q': b'Stub-Class', 'i': b'Unknown-Class'},
      {'n': 2, 'q': b'Unassessed-Class', 'i': b'Unknown-Class'}
  ]

  sort_imp = {
    b'High-Class': 300,
    b'Low-Class': 100,
    b'Mid-Class': 200,
    b'NA-Class': 25,
    b'NotA-Class': 21,
    b'Top-Class': 400,
    b'Unknown-Class': 0
  }

  sort_qual = {
    b'A-Class': 425,
    b'B-Class': 300,
    b'Book-Class': 55,
    b'C-Class': 225,
    b'Category-Class': 50,
    b'Disambig-Class': 48,
    b'FA-Class': 500,
    b'FL-Class': 480,
    b'FM-Class': 460,
    b'File-Class': 46,
    b'GA-Class': 400,
    b'Image-Class': 47,
    b'List-Class': 80,
    b'NA-Class': 25,
    b'NotA-Class': 21,
    b'Portal-Class': 45,
    b'Project-Class': 44,
    b'Redirect-Class': 43,
    b'Start-Class': 150,
    b'Stub-Class': 100,
    b'Template-Class': 40,
    b'Unassessed-Class': 0
  }

  def _insert_ratings(self):
    for r in self.ratings:
      rating = Rating(
        r_project=b'Test Project', r_namespace=0, r_article=r[0])
      rating.r_quality = r[1]
      rating.r_quality_timestamp = GLOBAL_TIMESTAMP_WIKI
      rating.r_importance = r[2]
      rating.r_importance_timestamp = GLOBAL_TIMESTAMP_WIKI

      with self.wp10db.cursor() as cursor:
        cursor.execute('INSERT INTO ' + Rating.table_name + '''
          (r_project, r_namespace, r_article, r_score, r_quality,
           r_quality_timestamp, r_importance, r_importance_timestamp)
          VALUES (%(r_project)s, %(r_namespace)s, %(r_article)s, %(r_score)s,
                  %(r_quality)s, %(r_quality_timestamp)s, %(r_importance)s,
                  %(r_importance_timestamp)s)
        ''', attr.asdict(rating))
      self.wp10db.commit()

  def _setup_global_articles(self):
    with self.wp10db.cursor() as cursor:
      for i, scores in enumerate(self.global_articles):
        cursor.execute('''
          INSERT INTO global_articles
            (a_article, a_quality, a_importance, a_score)
          VALUES (%s, %s, %s, %s)
        ''', ('Test Article %s' % i,) + scores)
    self.wp10db.commit()

  def _setup_project_categories(self):
    with self.wp10db.cursor() as cursor:
      cursor.executemany('INSERT INTO ' + Category.table_name + '''
          (c_project, c_type, c_rating, c_ranking, c_category, c_replacement)
        VALUES
          ('Catholicism', %(c_type)s, %(c_rating)s, %(c_ranking)s,
           %(c_category)s, %(c_rating)s)
      ''', self.project_categories)
    self.wp10db.commit()

  def setUp(self):
    super().setUp()
    self._setup_global_articles()
    self._insert_ratings()
    self._setup_project_categories()

  def test_get_global_stats(self):
    actual = tables.get_global_stats(self.wp10db)
    expected = [tuple(x.items()) for x in self.stats]
    actual = [tuple(x.items()) for x in actual]
    self.assertEqual(expected, actual)

  def test_get_project_stats(self):
    expected = [
      {'n': 3, 'q': b'FA-Class', 'i': b'Top-Class', 'project': b'Test Project'},
      {'n': 3, 'q': b'C-Class', 'i': b'Low-Class', 'project': b'Test Project'},
      {'n': 2, 'q': b'A-Class', 'i': b'High-Class', 'project': b'Test Project'},
      {'n': 3, 'q': b'B-Class', 'i': b'Low-Class', 'project': b'Test Project'},
      {'n': 2, 'q': b'FL-Class', 'i': b'High-Class', 'project': b'Test Project'},
      {'n': 3, 'q': b'GA-Class', 'i': b'Mid-Class', 'project': b'Test Project'},
      {'n': 1, 'q': b'FL-Class', 'i': b'Top-Class', 'project': b'Test Project'},
      {'n': 1, 'q': b'A-Class', 'i': b'Mid-Class', 'project': b'Test Project'}
    ]
    actual = tables.get_project_stats(self.wp10db, 'Test Project')
    expected = [tuple(x.items()) for x in expected]
    actual = [tuple(x.items()) for x in actual]
    self.assertEqual(sorted(expected), sorted(actual))

  def test_db_project_categories(self):
    actual = tables.db_project_categories(self.wp10db, b'Catholicism')
    expected = sorted(self.project_categories, key=lambda x: x['c_ranking'])
    actual = sorted(actual, key=lambda x: x['c_ranking'])
    self.assertEqual(expected, actual)

  def test_get_project_categories(self):
    expected = {
      'imp_labels': {b'High-Class': '{{High-Class}}',
                     b'Low-Class': '{{Low-Class}}',
                     b'Mid-Class': '{{Mid-Class}}',
                     b'NA-Class': '{{NA-Class}}',
                     b'NotA-Class': '{{NotA-Class}}',
                     b'Top-Class': '{{Top-Class}}',
                     b'Unassessed-Class': 'No-Class',
                     b'Unknown-Class': '{{Unknown-Class}}'},
      'qual_labels': {
        b'A-Class':
          '{{A-Class|category=Category:A-Class_Catholicism_articles}}',
        b'Assessed-Class':
          '{{Assessed-Class}}',
        b'B-Class':
          '{{B-Class|category=Category:B-Class_Catholicism_articles}}',
        b'Book-Class':
          '{{Book-Class|category=Category:Book-Class_Catholicism_articles}}',
        b'C-Class':
          '{{C-Class|category=Category:C-Class_Catholicism_articles}}',
        b'Category-Class':
          '{{Category-Class|category=Category:Category-Class_Catholicism_articles}}',
        b'Disambig-Class':
          '{{Disambig-Class|category=Category:Disambig-Class_Catholicism_articles}}',
        b'FA-Class':
          '{{FA-Class|category=Category:FA-Class_Catholicism_articles}}',
        b'FL-Class':
          '{{FL-Class|category=Category:FL-Class_Catholicism_articles}}',
        b'FM-Class':
          '{{FM-Class|category=Category:FM-Class_Catholicism_articles}}',
        b'File-Class':
          '{{File-Class|category=Category:File-Class_Catholicism_articles}}',
        b'GA-Class':
          '{{GA-Class|category=Category:GA-Class_Catholicism_articles}}',
        b'High-Class':
          '{{High-Class|category=Category:High-importance_Catholicism_articles}}',
        b'Image-Class':
          '{{Image-Class|category=Category:Category:Image-Class Catholicism articles}}',
        b'List-Class':
          '{{List-Class|category=Category:List-Class_Catholicism_articles}}',
        b'Low-Class':
          '{{Low-Class|category=Category:Low-importance_Catholicism_articles}}',
        b'Mid-Class':
          '{{Mid-Class|category=Category:Mid-importance_Catholicism_articles}}',
        b'NA-Class':
          '{{NA-Class|category=Category:NA-Class_Catholicism_articles}}',
        b'NotA-Class': ' style="text-align: center;" | ' "'''Other'''",
        b'Portal-Class':
          '{{Portal-Class|category=Category:Portal-Class_Catholicism_articles}}',
        b'Project-Class':
          '{{Project-Class|category=Category:Project-Class_Catholicism_articles}}',
        b'Redirect-Class':
          '{{Redirect-Class|category=Category:Redirect-Class_Catholicism_articles}}',
        b'Start-Class':
          '{{Start-Class|category=Category:Start-Class_Catholicism_articles}}',
        b'Stub-Class':
          '{{Stub-Class|category=Category:Stub-Class_Catholicism_articles}}',
        b'Template-Class':
          '{{Template-Class|category=Category:Template-Class_Catholicism_articles}}',
        b'Top-Class':
          '{{Top-Class|category=Category:Top-importance_Catholicism_articles}}',
        b'Unassessed-Class':
          '{{Unassessed-Class|category=Category:Unassessed_Catholicism_articles}}',
        b'Unknown-Class':
          '{{Unknown-Class|category=Category:Unknown-importance_Catholicism_articles}}'},
      'sort_imp': self.sort_imp,
      'sort_qual': self.sort_qual,
    }
    actual = tables.get_project_categories(self.wp10db, b'Catholicism')

    self.assertEqual(expected, actual)

  def test_data_for_stats(self):
    expected_cols = {
      b'High-Class': 1, b'Low-Class': 1, b'Mid-Class': 1, b'Unknown-Class': 1
    }
    expected_data = {b'C-Class': {b'Low-Class': 2, b'Unknown-Class': 1},
                     b'Start-Class': {b'High-Class': 3,
                                      b'Low-Class': 6,
                                      b'Mid-Class': 1,
                                      b'Unknown-Class': 1},
                     b'Stub-Class': {b'Low-Class': 3, b'Unknown-Class': 1},
                     b'Unassessed-Class': {b'Unknown-Class': 2}}

    actual_data, actual_cols = tables.data_for_stats(self.stats)
    actual_data_dict = dict((k, dict(v)) for k, v in actual_data.items())

    self.assertEqual(expected_cols, actual_cols)
    self.assertEqual(expected_data, actual_data_dict)

  def test_generate_table_data_removes_cols(self):
    missing_mid = dict(self.sort_imp)
    del missing_mid[b'Mid-Class']
    actual = tables.generate_table_data(self.stats, {
      'sort_imp': missing_mid, 'sort_qual': {},
      'imp_labels': {}, 'qual_labels': {}
    })

    self.assertTrue(b'Mid-Class' not in actual['ordered_cols'])

  def test_generate_table_data_removes_rows(self):
    missing_portal = dict(self.sort_qual)
    del missing_portal[b'Portal-Class']
    actual = tables.generate_table_data(self.stats, {
      'sort_imp': missing_portal, 'sort_qual': {},
      'imp_labels': {}, 'qual_labels': {}
    })

    self.assertTrue(b'Portal-Class' not in actual['ordered_rows'])

  def test_generate_table_data_adds_assessed_when_unassessed(self):
    actual = tables.generate_table_data(self.stats, {
      'sort_imp': self.sort_imp, 'sort_qual': self.sort_qual,
      'imp_labels': {}, 'qual_labels': {}
    })

    self.assertTrue(b'Unassessed-Class' in actual['ordered_rows'])
    self.assertTrue(b'Assessed-Class' in actual['ordered_rows'])
    unassessed_idx = actual['ordered_rows'].index(b'Unassessed-Class')
    actual_idx = actual['ordered_rows'].index(b'Assessed-Class')

    self.assertEqual(1, unassessed_idx - actual_idx)

  def test_generate_table_data_adds_assessed_when_no_unassessed(self):
    missing_unassessed = dict(self.sort_qual)
    del missing_unassessed[b'Unassessed-Class']
    actual = tables.generate_table_data(self.stats, {
      'sort_imp': self.sort_imp, 'sort_qual': missing_unassessed,
      'imp_labels': {}, 'qual_labels': {}
    })

    self.assertFalse(b'Unassessed-Class' in actual['ordered_rows'])
    self.assertTrue(b'Assessed-Class' in actual['ordered_rows'])
    self.assertEqual(
      len(actual['ordered_rows']) - 1,
      actual['ordered_rows'].index(b'Assessed-Class'))

  def test_generate_table_data_totals(self):
    expected_col_totals = {
      b'High-Class': 3,
      b'Low-Class': 11,
      b'Mid-Class': 1,
      b'Unknown-Class': 5
    }
    expected_row_totals = {
      b'Assessed-Class': 18,
      b'C-Class': 3,
      b'Start-Class': 11,
      b'Stub-Class': 4,
      b'Unassessed-Class': 2
    }

    actual = tables.generate_table_data(self.stats, {
      'sort_imp': self.sort_imp, 'sort_qual': self.sort_qual,
      'imp_labels': {}, 'qual_labels': {}
    })

    self.assertEqual(20, actual['total'])
    self.assertEqual(expected_col_totals, actual['col_totals'])
    self.assertEqual(expected_row_totals, actual['row_totals'])

  def test_generate_table_data_ordered_cols(self):
    expected = [b'High-Class', b'Mid-Class', b'Low-Class', b'Unknown-Class']
    actual = tables.generate_table_data(self.stats, {
      'sort_imp': self.sort_imp, 'sort_qual': self.sort_qual,
      'imp_labels': {}, 'qual_labels': {}
    })
    self.assertEqual(expected, actual['ordered_cols'])

  def test_generate_table_data_ordered_rows(self):
    expected = [
      b'C-Class',
      b'Start-Class',
      b'Stub-Class',
      b'Assessed-Class',
      b'Unassessed-Class'
    ]
    actual = tables.generate_table_data(self.stats, {
      'sort_imp': self.sort_imp, 'sort_qual': self.sort_qual,
      'imp_labels': {}, 'qual_labels': {}
    })
    self.assertEqual(expected, actual['ordered_rows'])

  def test_generate_table_data_labels(self):
    expected_imp_labels = {'foo': 'bar'}
    expected_qual_labels = {'baz': 'bang'}
    actual = tables.generate_table_data(self.stats, {
      'sort_imp': self.sort_imp, 'sort_qual': self.sort_qual,
      'imp_labels': expected_imp_labels, 'qual_labels': expected_qual_labels
    })

    self.assertEqual(expected_imp_labels, actual['col_labels'])
    self.assertEqual(expected_qual_labels, actual['row_labels'])

  def test_generate_table_data_table_overrides(self):
    expected_overrides = {'foo': 'bar', 42: 'answer', 'baz': 'bang'}
    actual = tables.generate_table_data(self.stats, {
      'sort_imp': self.sort_imp, 'sort_qual': self.sort_qual,
      'imp_labels': {}, 'qual_labels': {}
    }, table_overrides=expected_overrides)
    for k, v in expected_overrides.items():
      self.assertEqual(v, actual[k])

  def test_generate_project_table_data(self):
    actual = tables.generate_project_table_data(self.wp10db, b'Catholicism')
    self.assertEqual(
      'Catholicism articles by quality and importance', actual['title'])

  def test_generate_global_table_data(self):
    actual = tables.generate_global_table_data(self.wp10db)
    self.assertEqual(
      'All rated articles by quality and importance', actual['title'])

  @patch('lucky.tables.site')
  @patch('lucky.tables.wp10_connect')
  def test_upload_project_table(self, patched_connect, patched_site):
    try:
      orig_close = self.wp10db.close
      self.wp10db.close = lambda: True
      patched_connect.return_value = self.wp10db
      tables.upload_project_table(b'Catholicism')
    finally:
      self.wp10db.close = orig_close

  @patch('lucky.tables.site')
  @patch('lucky.tables.wp10_connect')
  def test_upload_global_table(self, patched_connect, patched_site):
    try:
      orig_close = self.wp10db.close
      self.wp10db.close = lambda: True
      patched_connect.return_value = self.wp10db
      tables.upload_global_table()
    finally:
      self.wp10db.close = orig_close