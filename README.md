# Flight_Ticket_Booking_DevRev

### It is the end to end fullstack project developed from scratch for DevRev Assignment

### Tech Stack:
Backend : Python Django Framework
Frontend : Bootstrap
Database : Sqlite3

### About the project:
It is an online flight ticket booking web application. 
This application contains two modules 
            * User
            * Admin
            
#### User modules:
  * **Register** - User can register by giving all the neccessary details and need to verify ##### Email before login.
  * **Login** - After successfully verified email, user can login into the profile page.
  * **Profile** - Profile page shows all the tickets booked by the user.
  * **Buy Tickets** - User can buy tickets on Buy tickets by and also apply filters to find flights.
  * **Search Flight** - User can search flights based on date and time.

#### Admin modules:
  * **Login** - Admin can login to the admin profile page by giving credentials( username : **admin** , password : **admin** ) in admin login page.
  * **Add Flights** - Admin can flights by giving fllight details.
  * **Remove Flights** - Admin can cancel flight.
  * **View Flights details** - Admin can view who are all the people booked tickets in   the selected flight.
 
#### Database design:
Django uses ORM(Object Relational Mapping) so all the models(objects) are created in Django itself.
There are totally 3 tables User, Flights and Flight_Book
User table has columns as 
           id
           name
           age
           contactno
           email
           password
           token - for **authentication** by setting **cache** in client browser
           is verified - for email verification status
Flights table has columns as
           flight _ number
           flight_namber
           flight _ from
           flight_to
           takeoff_date
           arrival_date
           takeoff_time
           arrival_time
           number_of_seats
           price
           seats_booked

Flight_Book table has columns as
           User - user object from User table
           Flight - flight object from Flight table
           
