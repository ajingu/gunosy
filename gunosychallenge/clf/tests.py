from django.test import TestCase

class ArticleClassifierTests(TestCase):
    """Test class for app"""
    
    def setUp(self):
        """Setup test"""
        self.categories = {'エンタメ',
                           'スポーツ',
                           'おもしろ',
                           '国内',
                           '海外',
                           'コラム',
                           'IT・科学',
                           'グルメ'}
    
    
    def test_get(self):
        """Accessing normally by 'get' method"""
        
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    
    def test_submit_correctly(self):
        """Correctly Submit form with url"""
        
        data = {
            'url': 'https://gunosy.com/articles/RiyqL',
        }
        
        response = self.client.post('/', data=data)
        self.assertEqual(response.status_code, 200)
        self.assertIn(response.context['result'], self.categories)
        
        
    def test_submit_incorrectly(self):
        """Incorrectly Submit form with url"""
        
        data = {
            'url': 'https://gunosy.com/',
        }
        
        response = self.client.post('/', data=data)
        self.assertEqual(response.status_code, 200)
        self.assertNotIn(response.context['result'], self.categories)