# Flight_Ticket_Booking_DevRev 

### It is the end to end fullstack project developed from scratch for DevRev Assignment
### webapp link : http://sanjay212.pythonanywhere.com/
### Tech Stack:
Backend : Python Django Framework <br>
Frontend : Bootstrap <br>
Database : Sqlite3 <br>

### About the project:
It is an online flight ticket booking web application. <br>
This application contains two modules <br>
            &emsp;* User<br>
            &emsp;* Admin<br>
            
#### User modules:
  * **Register** - User can register by giving all the neccessary details and need to verify ##### Email before login.
  * **Login** - After successfully verified email, user can login into the profile page by giving email and password.
  * **Profile** - Profile page shows all the tickets booked by the user.
  * **Buy Tickets** - User can buy tickets on Buy tickets by and also apply filters to find flights.
  * **Search Flight** - User can search flights based on date and time.

#### Admin modules:
  * **Login** - Admin can login to the admin profile page by giving credentials( username : **admin** , password : **admin** ) in admin login page.
  * **Add Flights** - Admin can flights by giving fllight details.
  * **Remove Flights** - Admin can cancel flight.
  * **View Flights details** - Admin can view who are all the people booked tickets in   the selected flight.
 
#### Database design:
Django uses ORM(Object Relational Mapping) so all the models(objects) are created in Django itself.<br>
There are totally 3 tables User, Flights and Flight_Book<br>
**User table has columns as** <br>
           &emsp;&emsp;id<br>
           &emsp;&emsp;name<br>
           &emsp;&emsp;age<br>
           &emsp;&emsp;contactno<br>
           &emsp;&emsp;email<br>
           &emsp;&emsp;password<br>
           &emsp;&emsp;token - for **authentication** by setting **cache** in client browser<br>
           &emsp;&emsp;is verified - for email verification status<br>
Flights table has columns as<br>
           &emsp;&emsp;flight _ number<br>
           &emsp;&emsp;flight_namber<br>
           &emsp;&emsp;flight _ from<br>
           &emsp;&emsp;flight_to<br>
           &emsp;&emsp;takeoff_date<br>
           &emsp;&emsp;arrival_date<br>
          &emsp; &emsp;takeoff_time<br>
           &emsp;&emsp;arrival_time<br>
           &emsp;&emsp;number_of_seats<br>
           &emsp;&emsp;price<br>
          &emsp; &emsp;seats_booked<br>

Flight_Book table has columns as<br>
          &emsp;&emsp; &emsp;User - user object from User table<br>
           &emsp;&emsp;&emsp;Flight - flight object from Flight table<br>
           
