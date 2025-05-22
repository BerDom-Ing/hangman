Feature: Hangman Game Web Application
  Como usuario
  Quiero jugar al ahorcado en una interfaz web
  Para divertirme adivinando palabras

  Scenario: Iniciar sesión con un nombre válido
    Given estoy en la página de inicio
    When ingreso el nombre "Jugador1"
    And hago clic en el botón "Comenzar"
    Then debería ver la página del juego
    And debería ver mi nombre "Jugador1" en la página

  Scenario: Iniciar un nuevo juego
    Given estoy logueado como "Jugador1"
    When accedo a la página del juego
    Then debería ver las vidas restantes
    And debería ver espacios para las letras de la palabra

  Scenario: Adivinar una letra correcta
    Given estoy logueado como "Jugador1"
    And estoy jugando una partida con la palabra "python"
    When adivino la letra "p"
    Then debería ver "p" en la primera posición de la palabra
    And mis vidas deberían seguir siendo 6

  Scenario: Adivinar una letra incorrecta
    Given estoy logueado como "Jugador1"
    And estoy jugando una partida con la palabra "python"
    When adivino la letra "a"
    Then no debería ver la letra "a" en la palabra
    And mis vidas deberían disminuir a 5

  Scenario: Ganar el juego
    Given estoy logueado como "Jugador1"
    And estoy jugando una partida con la palabra "cat"
    When adivino todas las letras "c", "a", "t"
    Then debería ver un mensaje de victoria
    And debería ver la opción para jugar de nuevo

  Scenario: Perder el juego
    Given estoy logueado como "Jugador1"
    And estoy jugando una partida con la palabra "python" y 3 vidas
    When adivino incorrectamente las letras "a", "b", "d"
    Then debería ver un mensaje de derrota
    And debería ver la palabra completa "python"
    And debería ver la opción para jugar de nuevo

  Scenario: Cerrar sesión
    Given estoy logueado como "Jugador1"
    When hago clic en "Cerrar sesión"
    Then debería volver a la página de inicio
    And no debería estar logueado