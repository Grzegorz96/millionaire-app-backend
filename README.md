![logo](https://raw.githubusercontent.com/Grzegorz96/millionaire-app-backend/master/docs/readme-images/logo.png)
# API for MILLIONAIRE.app and MILLIONAIRE.webapp

The Millionaire API enables users to establish a connection with the database directly from the frontend application. The program encompasses numerous endpoints necessary for the smooth functioning of the frontend. Additionally, it includes a JSON Web Token generator, a function securing endpoints, data input validation, a mechanism refreshing expired access tokens, and a tool for automatically sending generated activation numbers to email. The program is compatible with both Windows and Linux operating systems.


## Description of the modules

The program consists of 3 modules, each of which plays a unique role in the functioning of the application. Below is a brief description of each module:

API.py:
- The API.py module is responsible for handling requests, processing them, and returning responses. Additionally, this module generates JWT access tokens and JWT refresh tokens for newly logged-in users, refreshes expired access tokens, and secures certain endpoints that require access tokens. The functions on endpoints include validation for input data. This module is also responsible for direct operations on the MySQL database.

Database_conection.py:
- The Database_connection.py module is responsible for establishing a connection to the database, as required by the functions in the API.py module.

Activaiton_number_sender.py:
- The Activation_number_sender.py module is used to generate activation codes and send them to the specified email address.

For the program to function correctly, it also requires environmental variables defined in the .env file. All three modules retrieve necessary data and passwords from this file.


## Features

- A function that generates access tokens and refresh tokens.
- A function that protects endpoints against access by unauthorized persons.
- The function of sending the generated confirmation number to the user's e-mail address.
- The function of refreshing expired access tokens (15 minutes of validity) using an active refresh token (10 hours of validity).
- Database CRUD functions.
- Handling various errors and returning the appropriate code status.
- The function that checks whether the user refers to his ID number during the operation.
- Validation of all entered data.


## Technology used

**Server:** 
- Languages: Python, SQL
- Third Party Libraries: Flask, Flask-Cors, PyJWT, mysql-connector-python, python-dotenv
- Hosting for API: www.pythonanywhere.com
- Hosting for MySQL database: www.pythonanywhere.com


## Installation

### To run API on localhost:

#### Requirements:

##### Programs and libraries:
- Python 3.11.1
- IDE, for example Pycharm
- MySQL Server 8.0
- Flask 2.3.2
- Flask-Cors 4.0.0
- PyJWT 2.7.0
- mysql-connector-python 8.0.33
- python-dotenv 1.0.0

##### Environment Variables:

###### To run this project, you will need to add the following environment variables to your .env file:

`DATABASE_HOST`=IP or name of your host (127.0.0.1 or localhost).

`DATABASE_USER`=Your database username.

`DATABASE_PASSWORD`=Your database password.

`DATABASE_DATABASE`=The name of your database.

`API_SECRET_KEY`=Secret key for encoding and decoding your JSON Web Tokens.

```bash
# It is how to create your own SECRET_KEY variable.
import uuid
API_SECRET_KEY = uuid.uuid4().hex
```

`EMAIL_SENDER`=The email that will send messages to users.

`EMAIL_SENDER_PASSWORD`=Generated password for the given e-mail, in gmail u have to [turn on 2 step verification](https://myaccount.google.com/signinoptions/two-step-verification/enroll-welcome), then: 
###### - Go to your Google Account.
###### - Select Security.
###### - Under "Signing in to Google," select 2-Step Verification.
###### - At the bottom of the page, select App passwords.
###### - Enter a name that helps you remember where you’ll use the app password.
###### - Select Generate.
###### - To enter the app password, follow the instructions on your screen. The app password is the 16-character code that generates on your device.
###### - Select Done.


##### Tables for database:
- users
- top_scores
- questions
###### Login to your database and then copy and paste this text into your MySQL Workbench or MySQL Console.
```bash
CREATE TABLE `users` (
  `user_id` int NOT NULL AUTO_INCREMENT,
  `first_name` varchar(45) NOT NULL,
  `last_name` varchar(45) NOT NULL,
  `login` varchar(45) NOT NULL,
  `password` varchar(45) NOT NULL,
  `email` varchar(45) NOT NULL,
  `active_flag` tinyint NOT NULL DEFAULT '1',
  PRIMARY KEY (`user_id`),
  UNIQUE KEY `login_UNIQUE` (`login`),
  UNIQUE KEY `email_UNIQUE` (`email`)
```
  
```bash
CREATE TABLE `top_scores` (
  `top_score_id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `points` int NOT NULL,
  PRIMARY KEY (`top_score_id`),
  KEY `user_id_fk` (`user_id`),
  CONSTRAINT `user_id_fk` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`)
```

```bash
CREATE TABLE `questions` (
  `question_id` int NOT NULL AUTO_INCREMENT,
  `content` varchar(120) NOT NULL,
  `A` varchar(45) NOT NULL,
  `B` varchar(45) NOT NULL,
  `C` varchar(45) NOT NULL,
  `D` varchar(45) NOT NULL,
  `right_answer` varchar(1) NOT NULL,
  `difficulty` int NOT NULL,
  PRIMARY KEY (`question_id`),
  UNIQUE KEY `content_UNIQUE` (`content`)
```

```bash
INSERT INTO `questions` VALUES (1,'Sport wodny uprawiany na desce z żaglem to: ','skateboard','surfing','windsurfing','bojery','C',0),(2,'Kto był prezydentem Rzeczypospolitej Polskiej bezpośrednio przed Lechem Wałęsą ? ','Czesław Kiszczak ','Mieczysław Rakowski ','Wojciech Jaruzelski','Aleksander Kwaśniewski','C',1),(5,'Urządzenie służące do nagrywania i odtwarzania wiadomości w telefonie komórkowym to: ','toner ','faks ','poczta głosowa','poczta elektroniczna ','C',0),(6,'Powłoka na naczyniach kuchennych zapobiegająca przywieraniu potraw to: ','poliester ','teflon','akryl ','winyl ','B',0),(7,'Bohaterem jakiej powieści Henryka Sienkiewicza jest Jurand ze Spychowa ? ','„W pustyni i w puszczy” ','„Quo Vadis” ','„Potop” ','„Krzyżacy”','D',0),(8,'Kto został wiceprezesem Polskiego Związku Piłki Nożnej w 1999 roku ? ','Grzegorz Lato ','Zbigniew Boniek','Roman Kosecki ','Jan Tomaszewski ','B',0),(9,'Napój Anglików pijany tradycyjnie o piątej po południu to: ','oranżada ','kakao ','herbata','whisky ','C',0),(10,'W której z wymienionych dziedzin algi znalazły szerokie zastosowanie ? ','w budownictwie ','w kosmetyce','w obuwnictwie ','w dziewiarstwie ','B',0),(11,'Wywar rosołowy to: ','bulion','żur ','wassersuppe ','bulion Ureya ','A',0),(12,'Flausz to tkanina używana na: ','bluzki ','fartuchy ','płaszcze','sfetry','C',0),(13,'Daszek z wyciągiem umieszczony nad kuchnią, służący do usuwania zapachów na zewnątrz to: ','lufcik ','wywietrznik ','okap','szyber ','C',0),(14,'Jakie imię nosi największy dzwon w Polsce ? ','August ','Zygmunt','Kazimierz ','Bolesław ','B',1),(15,'Który z poetów polskich pisał: „O szyby deszcz dzwoni, deszcz dzwoni jesienny” ? ','Jan Kasprowicz ','Leopold Staff','Jan Lechoń ','Julian Tuwim ','B',1),(16,'W jakich jednostkach mierzy się długość i szerokość geograficzną ? ','godzinach i minutach ','metrach ','stopniach i minutach','milach ','C',1),(17,'Bawaria jest państwem związkowym: ','Francji ','Holandii ','Niemiec','Czech ','C',1),(18,'Jakie urządzenie służy do wykrywania, zapisywania i badania trzęsień ziemi ? ','polarymetr ','aerograf ','spektrometr ','sejsmograf','D',1),(19,'Zbieranie z powierzchni rosołu ściętego białka to: ','szumowanie','peklowanie ','szpikowanie ','marynowanie ','A',1),(20,'Kto był gospodarzem Mistrzostw Europy w piłce nożnej w 2000 roku ? ','Francja ','Włochy ','Holandia i Belgia','Niemcy ','C',2),(21,'Twórcą jakiego imperium był Czyngis-chan ? ','japońskiego ','chińskiego ','tatarskiego ','mongolskiego','D',1),(22,'Podwiązki służą do podtrzymywania: ','rajstop ','pończoch','spodni ','rajtuzów ','B',1),(23,'Nieprofesjonalny wykonawca roli aktorskiej w filmie to: ','naturalista ','kinoman ','dubler ','naturszczyk ','D',2),(24,'Pulchne placki drożdżowe smażone na oleju to: ','knedle ','naleśniki ','racuch','podpłomyki ','C',2),(25,'Janusz Kofta śpiewał, aby pamiętali: ','o pomnikach ','o kwiatach ','o najbliższych ','o ogrodach','D',2),(26,'Jak inaczej określa się osobę chorą na cukrzycę ? ','diabetyk','dyslektyk ','homeopata ','dietetyk ','A',2),(27,'Który z wymienionych metali wykorzystywany jest w termometrach ? ','rubid ','rod ','rtęć','ruten ','C',2),(28,'Statek wodny, na którego pokładzie mogą startować i lądować samoloty to: ','tankowiec ','krążownik ','niszczyciel ','lotniskowiec','D',2),(29,'Czworokąt, którego wszystkie boki są równe oraz wszystkie kąty proste to: ','prostokąt ','kwadrat','romb ','trapez ','B',2),(30,'Czego nie oznacza nazwa „koziorożec” ? ','znaku zodiaku ','zwrotnika ','sera z koziego mleka','kozła skalnego ','C',2),(31,'Gorące źródło wyrzucające w regularnych odstępach czasu wodę i parę wodną to: ','wulkan ','gejzer','bojler ','źródło artezyjskie ','B',3),(32,'Uszy którego ze zwierząt w gwarze myśliwskiej nazywane są „słuchami” ? ','tarpana ','żaby ','sarny ','zająca','D',2),(33,'Piaszczyste wzniesienie usypane przez wiatr to: ','piarg ','firn ','wydma','kopiec ','C',2),(34,'W jakim mieście znajduje się słynny 102-piętrowy wieżowiec Empire State Building ? ','w Londynie ','w Nowym Jorku','w Sydney ','w Ottawie ','B',2),(35,'Ptak wykorzystywany przez wojsko od starożytności do II wojny światowej do przenoszenia wiadomości to: ','bocian ','jastrząb ','gołąb','dzika gęś ','C',3),(36,'W jakich jednostkach mierzymy natężenie dźwięku ? ','w decybelach','w lumenach ','w kelwinach ','w amperach ','A',2),(37,'Depresja to obszar położony: ','1000 m n.p.m. ','500 m n.p.m. ','na poziomie morza ','poniżej poziomu morza','D',2),(38,'Haftka to rodzaj: ','ściegu ','agrafki ','suwaka ','zapinki','D',3),(39,'Miękka czapka wojskowa bez daszka, podłużnie składana to: ','rogatywka ','panama ','maciejówka ','furażerka','D',3),(40,'Nad jaką zatoką leży Półwysep Westerplatte ? ','Zatoką Gdańską','Zatoką Meklemburską ','Zatoką Pomorską ','Zatoką Ryską ','A',3),(41,'Ostatni przypadek w deklinacji polskiej to: ','wołacz','narzędnik ','miejscownik ','biernik ','A',3),(42,'Z jakiego tworzywa robiono okaryny ? ','ze stali ','z miedzi ','z gliny','z bakelitu ','C',4),(43,'Postać z włoskiej „commedia dell’ arte”, sprytna pokojówka, ukochana Arlekina to: ','Pulcinella ','Brighella ','Scaramuccia ','Kolombina','D',4),(44,'Na co „za komuny” nie było kartek ? ','na „Trybunę Ludu','na mięso ','na cukier ','na buty ','A',4),(45,'Jak nazywa się najwyższa skocznia narciarska ? ','żyrafia ','słoniowa ','mamucia','żurawia ','C',4),(46,'Ile wysokości ma stożek ? ','\'jedną\' ','dwie ','trzy ','cztery ','C',4),(47,'Litera „Ą” jest: ','samogłoską ustną ','samogłoską nosowa','spółgłoską dźwięczną ','spółgłoską bezdźwięczną ','B',4),(48,'Kto przez 5 lat mieszkał w wozie cyrkowym we wsi Podgradowice ? ','Jan Kiliński ','Andrzej Lepper ','Michał Drzymała','Jan Kierdziołek ','C',5),(49,'Woltyżerka to ćwiczenia akrobatyczne na koniu, biegnącym po obwodzie: ','kwadratu ','prostokąta ','trójkąta ','koła','D',5),(50,'Który z zespołów wylansował piosenkę pt. „Bal wszystkich świętych” ? ','Myslovitz ','T. Love ','Budka Suflera','Piersi ','C',5),(51,'Który z wymienionych dokumentów dotyczy samochodu ? ','dowód tożsamości ','REGON ','resurs ','dowód rejestracyjny','D',2),(52,'O kimś bez czupryny mówimy: ','łysy jak pośladek ','łysy jak pięta ','łysy jak kolano','łysy jak łokieć ','C',1),(53,'Ile było krasnoludków w bajce o Królewnie Śnieżce ? ','siedmiu','ośmiu ','dziewięciu ','dziesięciu ','A',0),(54,'Którą z potraw jadamy na ciepło ? ','auszpik ','melbę ','gulasz','sorbet ','C',3),(55,'Która z wymienionych liter jest czwartą literą w alfabecie greckim ? ','delta','lambda ','sigma ','omega ','A',6),(56,'Gody ryb to: ','toki ','ruja ','tarło','ciągi ','C',5),(57,'Co nie odmierza czasu ? ','gnomon ','klepsydra ','zegar ','kampanila','D',6),(58,'Który z podanych wyrazów nie określa figury w akrobacjach lotniczych ? ','pętla ','korkociąg ','otwieracz','beczka ','C',6),(59,'Ile trwa adwent – w chrześcijaństwie: okres przygotowań do Bożego Narodzenia ? ','2 tygodnie ','3 tygodnie ','4 tygodnie','pół roku ','C',6),(60,'Rodło – znak rodowy Polaków w Niemczech w stylizowanej formie odtwarza: ','bieg Odry ','bieg Wisły','bieg Łaby ','bieg Renu ','B',6),(61,'W którym kraju zachęca się rodziny do posiadania tylko jednego potomka ? ','w Rosji ','w Szwecji ','we Francji ','w Chinach','D',6),(62,'W biegu z przeszkodami zawodnicy skaczą przez: ','kozła ','mur ','żywopłot ','płotki','D',0),(63,'Przesądni odpukują w: ','szklaną kulę ','czoło czarnego kota ','talię kart ','niemalowane drewno','D',0),(64,'Półprosta wychodząca z wierzchołka kąta płaskiego i dzieląca go na dwie równe części to: ','dwusieczna','średnica ','krzywa ','cięciwa ','A',7),(65,'Który z wymienionych ptaków nie jest gatunkiem sowy ? ','puchacz ','puszczyk ','świstun','pójdźka ','C',7),(66,'W gwarze góralskiej człowiek z nizin to: ','cep ','kociuba ','ceper','cyntuś ','C',7),(67,'Biathlonista ma na nogach: ','narty biegowe','snowboard ','narty zjazdowe ','narty skokowe ','A',7),(68,'Potrawa z drobnych klusek gotowanych na mleku lub wodzie to: ','zalewajka ','zacierka','zasmażka ','mamałyga ','B',7),(69,'Ogary są psami: ','pasterskimi ','obronnymi ','gończymi','pociągowymi ','C',7),(70,'Jaki okrzyk wydawał kucharz Bartolini Bartłomiej, bohater dobranocki pt. „Porwanie Baltazara Gąbki” ? ','„Mamma Mia!” ','„Carramba!” ','„Kruca fuks!” ','„Ach, jooo!” ','A',7),(71,'Sok z jakich owoców musi wypić osoba dekorowana Orderem Uśmiechu ? ','z czarnej porzeczki ','z cytryny','z gruszki ','z marchwi ','B',7),(72,'Jaki kształt mają piramidy w Egipcie ? ','walca ','graniastosłupa ','ostrosłupa','prostopadłościanu ','C',3),(73,'Krajem przodującym w hodowli tulipanów i ich cebul jest: ','Holandia','Belgia ','Francja ','Szwecja ','A',2),(74,'Który z kamieni nie należy do szlachetnych ? ','nefryt','szmaragd ','szafir ','rubin ','A',7),(75,'Określony odcinek wyścigu kolarskiego to: ','etap','gem ','tercja ','runda ','A',1),(76,'Mieszkańcem rafy koralowej nie jest: ','ośmiornica ','ciernik','rozgwiazda ','gąbka ','B',7),(77,'Kto był wokalistą zespołu Led Zeppelin ? ','Robert Plant','John Lennon ','Mick Jagger ','Eric Burdon ','A',8),(78,'Popularna gra planszowa z kostką i płytkami z umieszczonymi na nich literami to: ','Domino ','Lotto ','Scrabble','Monopol ','C',0),(79,'Co nie należy do ekwipunku płetwonurka ? ','maska ','raki','butla z tlenem ','płetwy ','B',1),(80,'W piłce nożnej pierwsza żółta kartka pokazana przez sędziego głównego oznacza: ','wykluczenie z gry ','ostrzeżenie','spalony ','zmianę zawodnika ','B',0),(81,'Afrykański instrument muzyczny umożliwiający przekazywanie sygnałów na odległość to: ','tam-tam','drumla ','gong ','ksylofon ','A',8),(82,'Posąg Nike z Samotraki posiada: ','głowę ','ręce ','miecz ','skrzydła','D',8),(83,'Jaka postać nie została stworzona przez Walta Disneya ? ','Pszczółka Maja','Goofy ','Pluto ','Kaczor Donald ','A',3),(84,'Znaki drogowe w kształcie trójkąta, żółte z czerwonym obrzeżem to znaki: ','zakazu ','nakazu ','ostrzegawcze','informacyjne ','C',8),(85,'Na stadionie, a nie nad wodą, odbywają się zawody wędkarstwa: ','springowego ','spławikowego ','podlodowego ','rzutowego','D',8),(86,'Zgodnie z przesądem, małżeństwo będzie udane, jeśli panna młoda do ślubu założy: ','coś niemodnego ','coś pożyczonego','coś podartego ','coś czarnego ','B',8),(87,'Który z polskich polityków nie był premierem ? ','Tadeusz Mazowiecki ','Waldemar Pawlak ','Zofia Kuratowska','Jan Krzysztof Bielecki ','C',8),(88,'Która z wymienionych liczb jest podzielna przez 4 ? ','26 ','36','42 ','66 ','B',3),(89,'Jaka kopalnia znajduje się w Wieliczce ? ','kopalnia soli','kopalnia diamentów ','kopalnia miedzi ','kopania węgla kamiennego ','A',1),(90,'Który z motyli jest motylem nocnym ? ','paź królowej ','cytrynek ','pawik grabówka','bielinek kapustnik ','C',4),(91,'Kto był wokalistą zespołu The Doors ? ','Jim Morrison','Jimi Hendrix ','Eric Clapton ','Elvis Presley ','A',4),(92,'Jakiej narodowości jest Nadia Comaneci, 5-krotna mistrzyni olimpijska ? ','bułgarskiej ','węgierskiej ','rumuńskiej','czeskiej','C',5),(93,'Kanał Sueski stanowi umowną granicę między: ','Amerykami ','Afryką i Azją','Australią i Azją ','Kanadą i Grenlandią ','B',5),(94,'Jak w krawiectwie nazywa się rodzaj zapięcia działającego na zasadzie wtyczki i gniazda ? ','\'zatrzask\' ','rzep ','suwak ','haftka ','B',5),(95,'W którym filmie Romana Polańskiego, Mia Farrow spodziewa się dziecka diabła ? ','„Lokator” ','„Wstręt” ','„Matnia” ','„Dziecko Rosemary”','D',5),(96,'Kim według mitów greckich byli cyklopi ? ','żeglarzami ','władcami mórz ','jednookimi olbrzymami','bogami ','C',1),(97,'Kto stoi na czele korpusu dyplomatycznego akredytowanego w danym państwie ? ','dziekan','dyrektor ','rektor ','minister ','A',6),(98,'Konik morski to: ','szkarłupień ','ryba','mięczak ','głowonóg ','B',5),(99,'Sprawy codzienne, przyziemne to: ','chleb kamienny ','chleb świętojański ','chleb żałobny ','chleb powszedni','D',3),(100,'Gdzie w 1963 roku zastrzelono J. F. Kennedy’ego ? ','w Los Angeles ','w Dallas','w Atlancie ','w Phoenix ','B',9),(101,'W jaki sposób do lata zmierzała wokalistka zespołu Bajm – Beata Kozidrak ? ','piechotą','kajakiem ','autostopem ','hulajnogą ','A',9),(102,'Ilu było jeźdźców Apokalipsy ? ','dwóch ','trzech ','czterech','pięciu ','C',1),(103,'Która z podanych miar nie jest stosowana na morzu ? ','piędź','węzeł ','rumb ','kabel ','A',9),(104,'Jaki numer nosił Rudy – czołg „Czterej pancernych” ? ','101 ','102','202 ','303 ','B',2),(105,'Starożytni Rzymianie, mówiąc „mare nostrum” (nasze morze), mieli na myśli: ','Morze Kaspijskie ','Morze Czarne ','Morze Czerwone ','Morze Śródziemne','D',10),(106,'Którą z wymienionych książek dla dzieci napisał Jan Brzechwa ? ','Król Maciuś I ','Akademia Pana Kleksa','Biały Kieł ','Dzieci z Bullerbyn ','B',6),(107,'Ile kadłubów ma katamaran ? ','jeden ','dwa','trzy ','cztery ','B',1),(108,'Jaki płacz oznaczają „krokodyle łzy” ? ','szczery ','dyskretny ','histeryczny ','nieszczery','D',10),(109,'Ku czci jakiej bogini wzniesiono Partenon na Akropolu ateńskim ? ','Ateny','Artemidy ','Demeter ','Hery ','A',11),(110,'Nauczyciel języka obcego na wyższej uczelni to: ','adiunkt ','lektor','dziekan ','docent ','B',6),(111,'Wirtuozem gry na jakim instrumencie był Niccolo Paganini ? ','na waltorni ','na skrzypcach','na fortepianie ','na harfie ','B',11),(112,'Legendarny stwór o ciele uskrzydlonego lwa, głowie i szponach orła to: ','Gryf','Sfinks ','Centaur ','Minotaur ','A',5),(113,'Jak nazywa się znak w notacji muzycznej obniżający dźwięk o pół tonu ? ','synkopa ','krzyżyk ','bemol','fermata ','C',11),(114,'Piana z białek rozbita z cukrem i zapieczona w słodkie, białe ciastko to: ','makagigi ','strudel ','ptyś ','beza','D',5),(115,'Bez której z wymienionych przypraw nie może się obejść grzane wino ? ','bez chili ','bez cynamonu','bez piołunu ','bez curry ','B',4),(116,'Wianek panny młodej ozdobiony był dawniej: ','anyżkiem ','rutą','miętą ','macierzanką ','B',11),(117,'Które z podanych spodni są najdłuższe ? ','dzwony','szorty ','pludry ','bermudy ','A',10),(118,'Które z podanych miast leży nad Dunajem ? ','Nowy Targ ','Nowy Sad','Nowy Sącz ','Nowy Staw ','B',11),(119,'Szkarlatyna to inaczej: ','koklusz ','grypa ','płonica','malaria ','C',11),(120,'Czego nie produkują pszczoły ? ','mleczka ','kitu ','wosku ','nektaru','D',9),(121,'Kto porwał Piękną Helenę w utworze Homera pt. „Iliada” ? ','Agamemnon ','Achilles ','Parys','Hektor ','C',9),(122,'Kim był Louis Armstrong ? ','trębaczem jazzowym','astronautą ','pisarzem ','konstruktorem ','A',5),(123,'Jakie zwierzęta wyposażone są w kądziołki ? ','nietoperze ','kameleony ','modliszki ','pająki','D',10),(124,'Co nie jest ogrodzeniem ? ','ostrokół ','palisada ','zarzuela','zeriba ','C',10),(125,'Jakiego rodzaju artylerii użyli prawdopodobnie Krzyżacy w bitwie pod Grunwaldem ? ','haubic ','bombard','zenitówek ','pancerzownic ','B',11),(126,'Od końca XIX wieku kwintal liczył: ','10 kg ','100 kg','150 kg ','200 kg ','B',11),(127,'Co przypomina odgłos wydawany przez hienę ? ','mlaskanie ','chichot','mruczenie ','sapanie ','B',2),(128,'Powiedzenie „dziesiąta woda po kisielu” oznacza: ','mdły smak ','coś bardzo rzadkiego ','odległe pokrewieństwo','coś niesmacznego ','C',4),(129,'Ile „ramion” ma ośmiornica ? ','trzy ','pięć ','osiem','dwanaście ','C',3),(130,'W jakiej dyscyplinie sportowej Artur Partyka zdobył tytuł mistrza Europy w 1998 roku ? ','w skoku w wzwyż','w pchnięciu kulą ','w żeglarstwie ','w judo ','A',9),(131,'Z jakim ssakiem spokrewniony jest bizon ? ','z jeleniem ','z łosiem ','z sarną ','z żubrem','D',3),(132,'Jakiego koloru jest łódź podwodna w piosence zespołu The Beatles ? ','białego ','czarnego ','żółtego','niebieskiego ','C',7),(133,'W jakim mieście znajduje się Ściana Płaczu ? ','w Rzymie ','w Pekinie ','w Bombaju ','w Jerozolimie','D',5),(134,'Jakie lotnictwo zaatakowało Pearl Harbor 7 grudnia 1941 roku ? ','radzieckie ','włoskie ','japońskie','niemieckie ','C',3),(135,'W jakim kraju wynaleziono klocki Lego ? ','w USA ','w Danii','w Niemczech ','na Węgrzech ','B',7),(136,'W jakim budynku gospodarczym Augiasz miał największy bałagan ? ','w kurniku ','w chlewni ','w stodole ','w stajni','D',3),(137,'Bohaterem jakiej sztuki Bertolta Brechta jest Mackie Majcher ? ','„Matka Courage” ','„Kariera Artura Uli” ','„Życie Galileusza” ','„Opera za 3 grosze”','D',11),(138,'Jakiego zawodu uczy się bohaterka grana przez Jodie Foster w filmie pt. „Milczenie owiec” ? ','agentki FBI','modelki ','barmanki ','adwokata ','A',7),(139,'Latimeria to: ','ryba trzonopłetwa','taniec ','hiszpańska potrawa ','kobiece imię ','A',11),(140,'W dramacie Wyspiańskiego na wesele Chochoła zaprasza: ','Dziennikarz ','Czepiec ','Gospodarz ','Rachela','D',5),(141,'Organizacja światowa zrzeszająca narodowe związki piłkarskie to: ','NBA ','WBO ','WBC ','FIFA','D',3),(142,'Cichociemni działali w okresie: ','powstania styczniowego ','potopu szwedzkiego ','II wojny światowej','zimnej wojny ','C',9),(143,'Najbardziej „zakręcona” polska wokalistka to: ','Reni Jusis','Maryla Rodowicz ','Katarzyna Skrzynecka ','Agnieszka Chylińska ','A',6),(144,'Przeciwieństwem ascety jest: ','pokutnik ','sybaryta','biczownik ','męczennik ','B',8),(145,'Tak zwana dziura ozonowa to spadek zawartości ozonu: ','w oceanach ','w litosferze ','w atmosferze','w przestrzeni kosmicznej ','C',3),(146,'Który z podanych terminów nie określa części mózgu ? ','błona podstawna','szyszynka ','wzgórze ','przysadka ','A',11),(147,'W piłce ręcznej zawodnicy, poza bramkarzem, nie mogą dotykać piłki: ','odbitej przez przeciwnika ','głową ','tułowiem ','nogą poniżej kolana','D',6),(148,'W wojskach lądowych jedna gwiazdka na pagonie oznacza: ','kaprala ','chorążego','sierżanta ','plutonowego ','B',8),(149,'Ile naturalnych satelitów ma Ziemia ? ','jednego','dwóch ','trzech ','czterech ','A',3),(150,'„Nie rzucim ziemi, skąd nasz ród...” – tak zaczyna się: ','„Warszawianka” ','„Boże, cos Polskę” ','„Pierwsza Brygada” ','”Rota”','D',8),(151,'Jakiego koloru nie ma na fladze Belgii ? ','żółtego ','niebieskiego','czarnego ','czerwonego ','B',11),(152,'Urządzenie na pokładzie samolotu, pomagające ustalić przyczyny ewentualnej katastrofy to: ','trymer ','blue box ','czarna skrzynka','wolant ','C',0),(153,'Symbolem „hi-fi” oznaczamy: ','jakość obrazu ','jakość dźwięku','estetykę produktu ','wysoką cenę ','B',8),(154,'Wyborcy popierający określoną partię lub kandydata to: ','elektorat','publiczność ','audytorium ','respondenci ','A',0),(155,'Tytułowy bohater komedii pt. „Miś” jest prezesem klubu: ','„Wisła” ','„Słoneczko” ','„Tęcza”','„Warszawianka” ','C',10),(156,'Okresowy sprawdzian wiadomości studenta, najczęściej pisemny to: ','referat ','wypracowanie ','rozprawka ','kolokwium','D',8),(157,'Jak nazywa się zakonnik pilnujący drzwi w bramie klasztornej ? ','eremita ','oblat ','furtian','cenobita ','C',10),(158,'Reżyserem tanecznych układów widowisk scenicznych, szczególnie baletowych jest: ','choreograf','scenograf ','inscenizator ','inspicjent ','A',8),(159,'Co nie służy do kierowania wierzchowcem ? ','cugle ','lejce ','wodze ','popręg','D',9),(160,'Symbol chemiczny magnezu to: ','Mn ','Mg','Mo ','Md ','B',0),(161,'Ryszard Riedel śpiewał w zespole: ','Budka Suflera ','Elektryczne Gitary ','Dżem','Kombi ','C',9),(162,'Który ze znanych dziennikarzy grał postać Dudusia w serialu pt. „Podróż za jeden uśmiech” ? ','Tomasz Lis ','Wojciech Jagielski ','Maciej Orłoś ','Filip Łobodziński','D',10),(163,'Gdzie w organizmie ludzkim znajduje się plamka ślepa ? ','w oku','w mózgu ','w sercu ','w wątrobie ','A',9),(164,'Które z owadów nie są pod ochroną w Polsce ? ','jelonki rogacze ','modliszki zwyczajne ','biegacze ','bielinki kapustniki','D',10),(165,'Bohaterem jakiej powieści jest Cezary Baryka ? ','„Wierna rzeka” ','„Popioły” ','„Dzieje grzechu” ','„Przedwiośnia”','D',10),(166,'Norka jakiego zwierzęcia była bramą krainy czarów, do której trafiła Alicja ? ','królika','borsuka ','nornicy ','lisa ','A',9),(167,'Wywrócenie się samochodu lub samolotu do góry kołami to: ','kabotaż ','abordaż ','sabotaż ','kapotaż ','D',9),(168,'Przedstawiciel dyplomatyczny Watykanu w randze ambasadora to: ','kardynał ','nuncjusz','regent ','arcybiskup ','B',10),(169,'Która z pań nie była premierem ? ','Indira Gandhi ','Golda Meir ','Margaret Thatcher ','Zofia Kuratowska ','D',10),(170,'Niemiecka moneta zdawkowa to: ','grosch ','stotinka ','cent ','pfennig ','D',9),(171,'Ile razy Iga Świątek wygrała turniej Roland Garros','Jeden','Dwa','Trzy','Cztery','D',8);
```
#### Instruction:
- Download MySQL Server 8.0, install it on your computer and create a database.
- Optional install mysql workbench for easier database work.
- Create the required tables and add questions into questions database.
- Download millionaire-app-backend repository:
```bash
 git clone https://github.com/Grzegorz96/millionaire-app-backend.git
```
- Go to the millionaire-app-backend directory.
- Open the millionaire-app-backend on your IDE.
- Create .env file in your millionaire-app-backend directory.
- Add the required environment variables to the .env file.
- Create virtual enviroment for the project (Windows):
```bash
 py -m venv venv
```
- Create virtual enviroment for the project (Linux):
```bash
 python3 -m venv venv
```
- Activate virtual enviroment (Windows):
```bash
 venv/Scripts/activate.bat
```
- Activate virtual enviroment (Linux):
```bash
 source venv/bin/activate
```
- Install required packages on your activated virtual enviroment:
```bash
 pip install -r requirements.txt
```
- or
```bash
 pip install Flask==2.3.2
 pip install Flask-Cors==4.0.0
 pip install PyJWT==2.7.0
 pip install mysql-connector-python==8.0.33
 pip install python-dotenv==1.0.0
```
- Run API.py on Windows:
```bash
 py .\API.py
```
- Run API.py on Linux:
```bash
 python3 API.py
```
- Now your program run on port localhost:3000 u can change port by:
```bash
 app.run(debug=True, port=(set your own port))
```
- If you want connect desktop MILLIONAIRE.app program with local backend, you need to change endpoints in [millionaire-app-frontend/Backend_requests.py](https://github.com/Grzegorz96/millionaire-app-frontend/blob/master/Backend_requests.py) on:
```bash
 url = "http://localhost:3000/endpoint"
```
- Also when trying to connect Millionaire web app, change the endpoint urls in web application to the current one.
- If you want to query the API using your own application in a browser, you must add its domain to the CORS object in [millionaire-app-backend/API.py](https://github.com/Grzegorz96/millionaire-app-backend/blob/master/API.py), this will allow you to receive permission to use the returned data in the browser:
```bash
 CORS(app, resources={"*": {"origins": "https://your-own-domain.com"}})
```


## API Reference

#### HTTP GET METHODS:

##### 1. Endpoint to the function that retrieves questions from the database.
```http
  GET /questions
```
| Resource    | Type    | Description                |
| :--------   | :-------| :------------------------- |
| `questions` | `string`| **Required** Getting all questions from questions table. |

##### 2. Endpoint to the function that downloads scores from the database. 
```http
  GET /scores/?limit=
```
| Resource  | Type     | Description                | Parameter  | Type     | Description                |
| :-------- | :------- | :------------------------- | :-------- | :------- | :------------------------- |
| `scores`  | `string` | **Required** Getting users with their points from the database. | `limit`   | `int` | **Not Required** Specifying the limit of downloaded records. |

##### 3. (token required) Endpoint to the function that retrieves information about the logged in user from the database using the user id from the url and after validating the access token. HEADERS={"access-token":string, "refresh-token":string}.
```http
  GET /users/<int:user_id>  
```
| Resource  | Type     | Description                | Resource id | Type     | Description                |
| :-------- | :------- | :------------------------- | :--------- | :------- | :------------------------- |
| `users `  | `string` | **Required** Getting user data with given id. | `user_id`   | `int` | **Required** ID to specify the user. |

#### HTTP POST METHODS:

##### 1. Endpoint to the function that checks whether a user with the given login or email exists in the database. JSON={"login":string, "email":string}.
```http
  POST /users/register/check-data
```
| Resource  | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `users`   | `string` | **Required** Checking if the given user is not already in the database. |

##### 2. Endpoint to the function that sends the activation number to the user's e-mail address. JSON={"email_receiver":string}.
```http
  POST /users/send-activation-number
```
| Resource | Type    | Description                |
| :--------| :-------| :------------------------- |
| `users`  | `string`| **Required** Sending an e-mail to the address provided in the request body. |

##### 3. Endpoint to the function that adds a user to the database. JSON={"first_name":string, "last_name":string, "login":string, "password":string, "email":string}.
```http
  POST /users/register
```
| Resource | Type    | Description                |
| :--------| :-------| :------------------------- |
| `users`  | `string`| **Required** Inserting the given user data into a table in the database. |

##### 4. (token required) Endpoint to the function that adds the points earned by the user to the database. The function uses the JWT access token. HEADERS={"access-token":string, "refresh-token":string}. JSON={"user_id":integer, "points":integer}.
```http
  POST /scores
```
| Resource | Type    | Description                |
| :--------| :-------| :------------------------- |
| `scores` | `string`| **Required** Inserting points for a specific player in a table in the database. |

##### 5. (token required) Endpoint to the function that adds questions to the database. HEADERS={"access-token":string, "refresh-token":string}. JSON={"tresc":string, "odp":[string, string, string, string], "odp_poprawna":string, "trudnosc":integer} or JSON=[{},{}...].
```http
  POST /questions
```
| Resource    | Type    | Description                |
| :--------   | :-------| :------------------------- |
| `questions` | `string`| **Required** Inserting questions into a table in the database. |

##### 6. Endpoint to the function that retrieves the user's id from the database and creates an access token and a refresh token for it. JSON={"login":string, "password":string}.
```http
  POST /users/login
```
| Resource  | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `users`   | `string` | **Required** Retrieving generated JWT tokens and user id. |

#### HTTP PATCH METHODS:

##### 1. (token required) Endpoint to the function that update user information in the database. HEADERS={"access-token":string, "refresh-token":string}. JSON={"first_name":string} or JSON={"last_name":string} or JSON={"password":string}.
```http
  PATCH /users/<int:user_id>
```
| Resource  | Type     | Description                | Resource id | Type     | Description                |
| :-------- | :------- | :------------------------- | :---------- | :------- | :------------------------- |
| `users `  | `string` | **Required** Changing the user's data with the given id. | `user_id`   | `int` | **Required** ID to specify the user. |

#### HTTP DELETE METHODS:

##### 1. (token required) Endpoint to the function that delete user from the database. HEADERS={"access-token":string, "refresh-token":string}.
```http
  DELETE /users/<int:user_id>
```
| Resource  | Type     | Description                | Resource id | Type     | Description                |
| :-------- | :------- | :------------------------- | :---------- | :------- | :------------------------- |
| `users `  | `string` | **Required** Deleting a user with a given id. | `user_id`   | `int` | **Required** ID to specify the user. |


## Lessons learned

While creating the project, I acquired the skill of building a REST API. I have knowledge about working with JSON Web Tokens, and I know how to automatically send emails. Another challenge was implementing the backend application with a database on a web hosting platform to ensure seamless functionality. I strengthened my understanding of the SQL language and database operations. I learned how to integrate multiple programs using different technologies. I expanded my knowledge by working with .env files and gained insights into API, HTTP, SMTP, IPv4, localhost, and computer networks in general.


## Features to be implemented

- Hashing of user passwords in the database.
- Password recovery and change function via a code sent to email.
- Questions added should not go directly to the "questions" table, but first to a substitute table, and only after the administrator's verification should they be transferred to the main table.

## Authors

[@Grzegorz96](https://www.github.com/Grzegorz96)


## Contact

E-mail: grzesstrzeszewski@gmail.com


## License

[MIT](https://github.com/Grzegorz96/millionaire-app-backend/blob/master/LICENSE.md)


## Screnshoots
##### Users table
![users_table](https://raw.githubusercontent.com/Grzegorz96/millionaire-app-backend/master/docs/readme-images/users_table.png)
##### Questions table
![questions_table](https://raw.githubusercontent.com/Grzegorz96/millionaire-app-backend/master/docs/readme-images/questions_table.png)
##### Top scores table
![top_scores_table](https://raw.githubusercontent.com/Grzegorz96/millionaire-app-backend/master/docs/readme-images/top_scores_table.png)
##### Email sent from the email sender
![email_activation_number](https://raw.githubusercontent.com/Grzegorz96/millionaire-app-backend/master/docs/readme-images/email_activation_number.png)
