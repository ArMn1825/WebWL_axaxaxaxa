﻿# WebWL_axaxaxaxa<br />
Основной код в папке src<br />
Структура проекта: типовая структура java-приложения, исходники питона находятся в src/python<br />
src:<br />
----main Backend <br />
----python: // ML <br />
--------predict.py // основная программа<br />
--------output.csv // синтетический датасет<br />
--------input // пример json файла<br />
--------gen.py // генератор синтетического датасета<br />
--------model.py // неудачный вариант с нейронкой<br />
--------knn.py // тестирование knn<br />
<br />
Скомпилируйте проект в JAR:<br />
<br />
mvn clean package<br />
<br />
Найдите готовый JAR-файл в папке target.<br />
Запускайте приложение на Windows с помощью Java:<br />
<br />
java -jar my-application-1.0-SNAPSHOT.jar<br />
Сайт: localhost:42069<br />
Перед запуском питоновского скрипта убедитесь в наличии интерпретатора питона и библиотек pandas и sklearn у себя на ПК<br />

<br />
Запись: https://drive.google.com/drive/folders/1dVUgAn7CCMqAzQVlCXEIamk-63AcyRlj?usp=sharing<br />
Команда Хахатонщики<br />
Манухин Артем - Backend-разработчик<br />
Муксунов Тамдин - Data Scientist<br />
Бурик Сергей - советник<br />
