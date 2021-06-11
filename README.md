# Stocks n Gambling

I'd like to create a way for a user to compare how they would've done historically across picking stocks and picking sports teams.  So I'd like to have a "budget" that users can start with, then the ability to pick from stocks that they can buy (commission-free of course) and compare them with how they would do if they gambled on sports.  In addition, I'd like to create several bot users who:
- pick stocks/teams randomly
- pick stocks/teams according to some dumb machine learning model
- pick stocks/teams based on some novelty model (always bet against the Knicks, or something)

# Technical Components

The first part of this is a backing based on a database.  Because I run this on a kubernetes cluster running on Raspberry Pis, my db choices are limited to those that run on ARM.  So for this I picked MySql 8.0.

