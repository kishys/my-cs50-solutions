SELECT DISTINCT other_people.name
FROM people AS other_people
JOIN stars AS other_stars ON other_people.id = other_stars.person_id
JOIN movies AS other_movies ON other_stars.movie_id = other_movies.id
WHERE other_movies.id IN (
    SELECT movie_id
    FROM stars
    JOIN people ON stars.person_id = people.id
    WHERE people.name = 'Kevin Bacon' AND people.birthyear = 1958
) AND other_people.name != 'Kevin Bacon';
