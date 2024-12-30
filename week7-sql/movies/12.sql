SELECT movies.title
FROM movies
JOIN stars AS stars_cooper ON movies.id = stars_cooper.movie_id
JOIN stars AS stars_lawrence ON movies.id = stars_lawrence.movie_id
JOIN people AS cooper ON stars_cooper.person_id = cooper.id
JOIN people AS lawrence ON stars_lawrence.person_id = lawrence.id
WHERE cooper.name = 'Bradley Cooper' AND lawrence.name = 'Jennifer Lawrence';
