SELECT DISTINCT people.name
FROM people
JOIN directors ON people.id = directors.person_id
JOIN movies ON directors.movie_id = movies.id
WHERE movies.imdb_rating >= 9.0;
