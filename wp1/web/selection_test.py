import unittest
from wp1.web.app import create_app


class ProjectTest(unittest.TestCase):

  invalid_article_name = "Eiffel_Tower\nStatue of#Liberty"
  unsuccessful_response = {
      "success": False,
      "items": {
          'valid': ['Eiffel_Tower'],
          'invalid': ['Statue_of#Liberty'],
          'forbiden_chars': ['#']
      }
  }
  valid_article_name = "Eiffel_Tower\nStatue of Liberty"
  successful_response = {"success": True, "items": {}}

  def test_create_unsuccessful(self):
    self.app = create_app()
    with self.app.test_client() as client:
      rv = client.post('/v1/selection/simple',
                       json={
                           'articles': self.invalid_article_name,
                           'list_name': 'my_list',
                           'project': 'my_project'
                       })
      self.assertEqual(rv.get_json(), self.unsuccessful_response)

  def test_create_successful(self):
    self.app = create_app()
    with self.app.test_client() as client:
      rv = client.post('/v1/selection/simple',
                       json={
                           'articles': self.valid_article_name,
                           'list_name': 'my_list',
                           'project': 'my_project'
                       })
      self.assertEqual(rv.get_json(), self.successful_response)

  def test_empty_article(self):
    self.app = create_app()
    with self.app.test_client() as client:
      rv = client.post('/v1/selection/simple',
                       json={
                           'articles': '',
                           'list_name': 'my_list',
                           'project': 'my_project'
                       })
    self.assertEqual(rv.status, '400 BAD REQUEST')

  def test_empty_list(self):
    self.app = create_app()
    with self.app.test_client() as client:
      rv = client.post('/v1/selection/simple',
                       json={
                           'articles': self.valid_article_name,
                           'list_name': '',
                           'project': 'my_project'
                       })
    self.assertEqual(rv.status, '400 BAD REQUEST')

  def test_empty_project(self):
    self.app = create_app()
    with self.app.test_client() as client:
      rv = client.post('/v1/selection/simple',
                       json={
                           'articles': self.valid_article_name,
                           'list_name': 'my_list',
                           'project': ''
                       })
    self.assertEqual(rv.status, '400 BAD REQUEST')
