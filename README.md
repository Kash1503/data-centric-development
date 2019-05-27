# Data Centric Development Milestone Project

This is a website designed to allow users to create, view, edit and delete food recipes. The website will store the recipes they have created and display these in lists for the user to interact with.


## UX

This project is aimed at cooking enthusiasts, students living alone and parents looking for something to cook for their family. I have attempted to keep the design and interactivity simple and intuitive enough that anybody can make sense of it and make use of the site. 
As the site is aimed at those who may not be so computer literate, I have attempted to design the UX in such a way that it is easy to read and understand, showing relevant information and pointing users to the various features of the site. 

### User Stories

- As a user, I want to be able to create a login to add my own recipes (epic)
  - As a user, I want to be able to add, edit and delete my recipes
  - As a user, I want to be able to see the recipes I have made

- As a user, I want to browse through existing recipes (epic)
  - As a user, I want to be able to filter through the existing recipes to find what I am looking for
  - As a user, I want to see statistical information about the existing recipes
  - As a user, I want to be able to filter through the statistical information to find what I am looking for

- As a user, I want to be able to easily navigate the site
  - As a user, I want to be able to go from viewing my own recipes to browsing all the recipes easily
  - As a user, I want to be able to quickly and easily add, edit or delete a recipe

- As a user, I want to see detailed information about the recipe (epic)
  - As a user, I want to know how many people have viewed this recipe
  - As a user, I want to be able to see how many people liked the recipe
  - As a user, I want to know how long the recipe will take to make
  - As a user, I want to know what ingredients I will need
  - As a user, I want instructions on how to make the recipe
  - As a user, I want to see the nutritional information of the recipe
  - As a user, I want to see who wrote the recipe
  - As a user, I want to be able to select the author and their other recipes
  - As a user, I want to see how many people the recipe will serve
  - As a user, I want to see if there are any allergens in the recipe
  - As a user, I want to know what type of cuisine the recipe belongs to

### Planning 

Wireframes and other documentation is stored in the [Planning Folder](planning)


## Features

### Existing features

- User registration: Allows users to create their own profile, so that they can create, edit and view recipes on the site.
- User login: Login page to allow users to access their recipes and home page.
- Add recipe: Allows users to add a recipe, adding it to the database.
- Edit recipe: Allows users to edit existing recipes they have created.
- Delete recipe: Allows users to delete recipes they have created.
- Browse recipes: Users can browse all of the recipes created by all users.
- Filter recipes by attribute: Users are able to filter the list of recipes presented to them, in order to find the recipe they want.
- Statistics view/visualisation: Analytics data visible for all users to see a breakdown of top level data about the recipes currently held in the datatbase.
- Detailed view for recipes: A detailed view of each individual recipe, including instructions, ingredients and nutrition information about the chosen recipe.

### Features ideas yet to be added

- Pagination: If the list were to grow too large it may cause bad UX for the user.
- Recipe rating: An overall rating for each recipe based on reviews.
- Comments section: Users would be able to leave comments for a recipe.
- Password for user profile: Users would set a password for their profile, keeping it secure.
- Current page could be highlighted on the Nav to ensure users know which part of the site they currently reside on.
- The sliders included on the forms could show the current number value of the slider for better UX.
- Ability for user to bullet point ingredient and instructions.
- Ability to add muliple allergens to a recipe.
- User should only be able to like a recipe once.


## Technologies Used

- [Materialize v0.100.2](http://archives.materializecss.com/0.100.2/)
  - The project uses Materialize for styling and the grid system
- [Material Icons](https://material.io/tools/icons/?style=baseline)
  - Material Icons used for the various icons used throughout the site
- [jQuery](http://jquery.com/)
  - jQuery has been used to assist in the styling and creating the charts
- [D3.js](https://d3js.org/)
- [DC.js](https://dc-js.github.io/dc.js/)
- [Crossfilter](https://square.github.io/crossfilter/)
  - D3.js, DC.js and Crossfilter have been used to create the graphs for the Analytics page
- [MongoDB](https://www.mongodb.com/)
  - Used MongoDB for the database which holds the user and recipe information

## Testing

All testing completed on Safari and Google Chrome at both mobile and desktop size on macbook pro and iphone XR. Unable to see difference between browsers tested on.

*Manual Testing*

1. Login Page:
 - Go to the 'Login' page
 - Attempted to submit an empty form
 - Attempted to input invalid username
 - Attempted to input valid username

2. Register Page:
 - Go to the 'Register' page
 - Attempted to submit empty form
 - Attempted to submit partially complete form
 - Attempted to register with username which is already in use
 - Attempted to register a new user with a new username
 - Tested all buttons visible on the page

3. User/Home Page:
 - Go to the 'User/Home' page
 - Ensured that the visible recipes have all been created by this user
 - Test all filter options

4. Browse Page:
 - Go to the 'Browse' page
 - Test the filter options individually
 - Ensured that the list of recipes are from all users
 - Ensured that recipes were clickable and information was correct

5. Recipe Details Page:
 - Go to the 'Recipe Details' Page
 - Ensured that the information visible was displaying correctly and was accurate
 - Test the 'Like' Button
 - Ensured that the 'Like' Button was only clickable for recipes I had not created

6. Add/Edit Recipe Pages:
 - Go to the 'Add/Edit Recipe' page
 - Attmped to submit an empty form
 - Attempted to submit a partially complete form
 - Attempted to submit a complete form
 - Ensured that the recipe was added to the database once submitted
 - Tested all buttons visible on page

7. Analytics Page:
 - Go to the 'Analytics' page
 - Ensured that all data was accurate according to the data held in the database
 - Ensure that the 'test' database entries were not included in the data displayed

*Automatic Testing*

To run the automatic tests, please use the command 'python3 test.py' in the console. All tests should pass.

*Bugs*

Encountered various bugs while testing:

- Bug found when testing the 'Analytics' page where the data included data from the 'test' recipe data.
- Had an issue on the 'Recipe Details' page where the 'Go Back' button would always return the user to the home page, rather than the page they had come from.
- Had styling issues throughout regarding responsive design

## Deployment

In order to deploy this project, regular commits were made to the Github repository and then using Heroku I was able to deploy the website. No apparent difference between development and deployed builds.

I have only used one Git branch to develop and deploy this project. 

[Click here to go to the website](https://data-centric-design.herokuapp.com/)

### Content

Content I have used in populating the database for test purposes include images taken from google searches, ensuring that the licence allows for use. 

- [Chicken Masala Image](https://upload.wikimedia.org/wikipedia/commons/thumb/f/f5/A_shot_of_butter_chicken_masala.jpg/1600px-A_shot_of_butter_chicken_masala.jpg)
- [Pasta Bolognese Image](https://upload.wikimedia.org/wikipedia/commons/thumb/9/9a/Pasta_Bolognese_%28CC%29_%2810140854694%29.jpg/1599px-Pasta_Bolognese_%28CC%29_%2810140854694%29.jpg)
- [Teriyaki Chicken recipe](https://upload.wikimedia.org/wikipedia/commons/a/ab/Gfp-chinese-teriyaki-chicken.jpg)
- [Baked Salmon Image](https://live.staticflickr.com/3862/14395796846_f6e5558384_b.jpg)

### Acknowledgments

Inspiration was taken from the following: 

- [Cook For Your Life](https://www.cookforyourlife.org/)
- [BBC Good Food](https://www.bbcgoodfood.com/recipes/category/dishes)
- [Jamie Oliver](https://www.jamieoliver.com/recipes/category/world/italian/)
- [All Recipes](https://www.allrecipes.com/recipes/17562/dinner/)