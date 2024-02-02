<h1 align="center">
  <img src="images/banner.svg" alt="Cube API"/>
  Cube API
  <br/>
</h1>

<p align="center">
    Rest API, которое используется в сервисах CubeStudio.
</p>

## Последний релиз: 0.1
* Первый запуск Cube-API 🎉
* Запуск /api/v1/get_compiled_instance

## Дорожная карта версий
* [X] 0.1: Первый запуск Cube-API
* [ ] 0.2: Создать Cube-CLI
* [ ] 0.3: Добавить поддержку CurseForge
* [ ] 0.4: Добавить поддержку множества Instances одновременно
* [ ] 0.5: Поддержка будущего CubeBadges*

## Стек проекта
* ```FastAPI```
* ```uvicorn```
* ```Pydantic```

## Полезные ссылки
* Телеграм-канал CubeStudio: https://t.me/+Gphg_BIJEdMwMmFi
* Сайт CubeStudio: [fadegor05.github.io/CubeStudio/](https://fadegor05.github.io/CubeStudio/)
* CubeStart: https://github.com/fadegor05/Cube-Start

## Как работают Instance?
Что такое Instance? Instance - это один из новых уникальных и простых способов передачи сборки на устройство участника проекта CubeShield, настройка сборки происходит в файле ```instance.json```, который обязательно должен находится в корневой папке проекта, этот файл имеет данное содержание:
```
{
	"id": 0, // Айди проекта (Необходимо менять для каждой новой сборки)
  "name": "CubeShield Experiment: Example", // Название сборки
  "version": "0.0.1", // Версия сборки (Необходимо менять для применения изменений для всех игроков)
  "changelog": "", // Изменения версии
  "game_version": "1.20.4", // Версия Minecraft
  "loader": "fabric", // Загрузчик Minecraft
  "modrinth": [ // Моды с сайта Modrinth
    {
      "mod": "simple-voice-chat", // Slug или ID мода
      "version": "fabric-1.20.4-2.5.1" // Slug или ID версии мода (все можно найти в строке поиска, при открытом моде)
    },
    {
      "mod": "...",
      "version": "..."
    },
  ]
}
```

## Переменные среды
```API_KEY = ...``` - секретный ключ для будующих интеграций

## Деплой (Development)
* ```git clone ...```
* ```poetry update```
* ```poetry run sh start.sh```
<br>
или
<br>
* ```git clone ...```
* ```poetry update```
* ```poetry shell```
* ```uvicorn app:create_app --port 8000```

## Деплой (Production)
* TODO
###### Not an official Minecraft product. We are in no way affiliated with or endorsed by Mojang Synergies AB, Microsoft Corporation or other rightsholders.