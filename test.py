import os
import unittest
from bson.objectid import ObjectId
from app import app, mongo

test_user_data = {
    'username': 'test',
    'firstname': 'testfirst',
    'lastname': 'testlast',
    'country': 'testcountry'
}

test_recipe_data = {
    'title': 'testrecipe001',
    'instructions': 'testinstructions',
    'ingredients': 'testingredients',
    'servings': '1',
    'time': '20',
    'cuisine': 'testcuisine',
    'description': 'testdescription',
    'allergen': 'testallergen',
    'carbs': '50',
    'protein': '50',
    'fat': '50',
    'calories': '100',
    'imageURL': 'https://upload.wikimedia.org/wikipedia/commons/6/6d/Good_Food_Display_-_NCI_Visuals_Online.jpg'
}

test_update_recipe_data = {
    'title': 'testrecipe',
    'instructions': 'testinstructions',
    'ingredients': 'testingredients',
    'servings': '1',
    'time': '20',
    'cuisine': 'testcuisine',
    'description': 'testdescription',
    'allergen': 'testallergen',
    'carbs': '50',
    'protein': '50',
    'fat': '50',
    'calories': '100',
    'imageURL': 'https://upload.wikimedia.org/wikipedia/commons/6/6d/Good_Food_Display_-_NCI_Visuals_Online.jpg'
}

test_delete_recipe_data = {
    '_id': ObjectId('2f1ebf38bcee491dd7187c25'),
    'title': 'testdelete',
    'instructions': 'test',
    'ingredients': 'test',
    'servings': 5,
    'time': 50,
    'cuisine': 'test',
    'views': 0,
    'user': 'testuser',
    'description': 'test',
    'allergen': 'test',
    'upvotes': 0,
    'carbs': 50,
    'protein': 50,
    'fat': 50,
    'calories': 50,
    'isTest': 'False',
    'imageURL': 'https://upload.wikimedia.org/wikipedia/commons/6/6d/Good_Food_Display_-_NCI_Visuals_Online.jpg'
}

test_filter_data_cuisine_only = {
    'cuisine': 'indian',
    'allergens': 'all',
    'time': '0-180',
    'servings': '0-20',
    'calories': '0-1000'
}

test_filter_data_allergen_only = {
    'cuisine': 'all',
    'allergens': 'fish',
    'time': '0-180',
    'servings': '0-20',
    'calories': '0-1000'
}

test_filter_data_cuisine_and_allergen = {
    'cuisine': 'indian',
    'allergens': 'fish',
    'time': '0-180',
    'servings': '0-20',
    'calories': '0-1000'
}

class BasicTests(unittest.TestCase):
    
    """set up and tear down functions"""
    
    def setUp(self):
        app.config['TESTING'] = True
        app.config['DEBUG'] = False
        self.app = app.test_client()
 
    def tearDown(self):
        pass
    
    
    """Tests"""
    
    def test_main_page(self):
        response = self.app.get('/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
    
    def test_login_page(self):
        response = self.app.get('/login', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
    
    def test_register_page(self):
        response = self.app.get('/register', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
    
    def test_add_recipe_page(self):
        response = self.app.get('/add_recipe/<username>', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
    
    def test_edit_recipe_page(self):
        response = self.app.get('/edit_recipe', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        
    def test_user_page(self):
        response = self.app.get('/user_page', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
    
    def test_browse_page(self):
        response = self.app.get('/browse', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        
    def test_recipe_details_page(self):
        response = self.app.get('/recipe_details', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        
    def test_insert_user_function(self):
        response = self.app.post('/insert_user', data=test_user_data, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        mongo.db.user.remove({'username': 'test'})
        
    def test_get_user_function_with_invalid_username(self):
        response = self.app.post('/get_user', data={'username': 'test'}, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
    
    def test_get_user_function_with_valid_username(self):
        mongo.db.user.insert_one(test_user_data)
        response = self.app.post('/get_user', data={'username': 'test'}, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        mongo.db.user.remove({'username': 'test'})
    
    def test_insert_recipe_function(self):
        response = self.app.post('/insert_recipe', data=test_recipe_data, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        mongo.db.recipes.remove({'title': 'testrecipe001'})
    
    def test_update_recipe_function(self):
        response = self.app.post('/update_recipe', data=test_update_recipe_data, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
    
    def test_delete_recipe_function(self):
        mongo.db.recipes.insert_one(test_delete_recipe_data)
        response = self.app.get('/delete_recipe', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        
    def test_filter_recipes_function_cuisine_only(self):
        response = self.app.post('/filter_recipes', data=test_filter_data_cuisine_only, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
    
    def test_filter_recipes_function_allergen_only(self):
        response = self.app.post('/filter_recipes', data=test_filter_data_allergen_only, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
    
    def test_filter_recipes_function_cuisine_and_allergen(self):
        response = self.app.post('/filter_recipes', data=test_filter_data_cuisine_and_allergen, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
    
    def test_upvote_function(self):
        response = self.app.get('/upvote', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
    
    def test_create_graph_data_function(self):
        response = self.app.get('/create_graph_data', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        
    def test_analytics_page(self):
        response = self.app.get('/analytics_page/<username>', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        
if __name__ == '__main__':
    unittest.main()