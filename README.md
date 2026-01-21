<!-- Improved compatibility of back to top link: See: https://github.com/othneildrew/Best-README-Template/pull/73 -->
<a name="readme-top"></a>
<!--
*** Thanks for checking out the Best-README-Template. If you have a suggestion
*** that would make this better, please fork the repo and create a pull request
*** or simply open an issue with the tag "enhancement".
*** Don't forget to give the project a star!
*** Thanks again! Now go create something AMAZING! :D
-->



<!-- PROJECT SHIELDS -->
<!--
*** I'm using markdown "reference style" links for readability.
*** Reference links are enclosed in brackets [ ] instead of parentheses ( ).
*** See the bottom of this document for the declaration of the reference variables
*** for contributors-url, forks-url, etc. This is an optional, concise syntax you may use.
*** https://www.markdownguide.org/basic-syntax/#reference-style-links
-->
[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]
[![LinkedIn][linkedin-shield]][linkedin-url]



<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/Novanglus96/{{PROJECT_NAME}}">
    <img src="frontend/public/logov2.png" alt="Logo" height="40">
  </a>

<h3 align="center">{{PROJECT_NAME}}</h3>

  <p align="center">
  A template for Django/Vue/Docker projects
    <br />
    <a href="https://github.com/Novanglus96/{{PROJECT_NAME}}"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="https://github.com/Novanglus96/{{PROJECT_NAME}}/issues/new?template=bug_report.md">Report Bug</a>
    ·
    <a href="https://github.com/Novanglus96/{{PROJECT_NAME}}/issues/new?template=feature_request.md">Request Feature</a>
  </p>
</div>



<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

[![Product Name Screen Shot][product-screenshot]](https://example.com)

A template for Django/Vue/Docker projects.  Please read instructions.txt for insutructions on how to use this template.

<p align="right">(<a href="#readme-top">back to top</a>)</p>


 
### Built With

* [![Django][Django]][Django-url]
* [![Vue][Vue.js]][Vue-url]
* [![Docker][Docker]][Docker-url]

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- GETTING STARTED -->
## Getting Started

Welcome to {{PROJECT_NAME}}! This guide will help you set up and run the application using Docker and Docker Compose.

### Prerequisites

Make sure you have the following installed on your system:

* [Docker](https://www.docker.com/get-started)
* [Docker Compose](https://docs.docker.com/compose/install/)

<!-- INSTALLATION -->
### Step 1: Create a `.env` File

Create a `.env` file in the root directory of the project. This file will store environment variables required to run the application. Below is an example of the variables you need to define:

```env
DEBUG=0
SECRET_KEY=mysupersecretkey
DJANGO_ALLOWED_HOSTS=localhost
CSRF_TRUSTED_ORIGINS=http://localhost
SQL_ENGINE=django.db.backends.postgresql
SQL_DATABASE={{PROJECT_NAME}}
SQL_USER={{PROJECT_SLUG}}user
SQL_PASSWORD=somepassword
SQL_HOST=db
SQL_PORT=5432
DATABASE=postgres
DJANGO_SUPERUSER_PASSWORD=suepervisorpassword
DJANGO_SUPERUSER_EMAIL=someone@somewhere.com
DJANGO_SUPERUSER_USERNAME=supervisor
VITE_API_KEY=someapikey
TIMEZONE=America/New_York
```

Adjust these values according to your environment and application requirements.

### Step 2: Create a `docker-compose.yml` File

Create a `docker-compose.yml` file in the root directory of the project. Below is an example configuration:

```yaml
services:
  frontend:
    image: {{PROJECT_SLUG}}_frontend:production
    container_name: {{PROJECT_SLUG}}_frontend
    networks:
      - default
    restart: unless-stopped
    expose:
      - 80
    env_file:
      - ./.env
    environment:
      - TIMEZONE=America/New_York
      - TZ=${TIMEZONE}
  backend:
    image: {{PROJECT_SLUG}}_backend:production
    container_name: {{PROJECT_SLUG}}_backend
    command: /home/app/web/start.sh
    volumes:
      - static_volume:/home/app/web/staticfiles
      - media_volume:/home/app/web/mediafiles
      - postgres_bkp:/backups/
    expose:
      - 8000
    depends_on:
      - db
    networks:
      - default
      - backend
    env_file:
      - ./.env
  worker:
    image: {{PROJECT_SLUG}}_worker:production
    container_name: {{PROJECT_SLUG}}_worker
    command: /home/app/web/start_worker.sh
    volumes:
      - static_volume:/home/app/web/staticfiles
      - media_volume:/home/app/web/mediafiles
      - postgres_bkp:/backups/
    depends_on:
      - db
      - backend
    networks:
      - default
      - backend
    env_file:
      - ./.env
  db:
    image: postgres:18-trixie
    container_name: {{PROJECT_SLUG}}_db
    volumes:
      - postgres_data:/var/lib/postgresql/data/
    env_file:
      - ./.env
    networks:
      - default
      - backend
    environment:
      - TZ=UTC
      - POSTGRES_USER=${SQL_USER}
      - POSTGRES_PASSWORD=${SQL_PASSWORD}
      - POSTGRES_DB=${SQL_DATABASE}
  nginx:
    image: novanglus96/lenoreapps_proxy:latest
    container_name: {{PROJECT_SLUG}}_proxy
    volumes:
      - static_volume:/home/app/web/staticfiles
      - media_volume:/home/app/web/mediafiles
    depends_on:
      - backend
      - frontend
    networks:
      - default
    ports:
      - 7000:80
    environment:
      - TZ=${TIMEZONE}

volumes:
  postgres_data:
  static_volume:
  media_volume:
  postgres_bkp:
   
networks:
  backend:
    internal: true
```

### Step 3: Run the Application

1. Start the services:

   ```bash
   docker compose up -d
   ```

2. Access the application in your browser at `http://localhost:8080`.

### Notes

* Adjust exposed ports as needed for your environment.
* If you encounter any issues, ensure your `.env` file has the correct values and your Docker and Docker Compose installations are up to date.

Enjoy using {{PROJECT_NAME}}!

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- USAGE EXAMPLES -->
## Usage
See the full <a href="https://novanglus96.github.io/{{PROJECT_NAME}}"><strong>documentation</strong></a>.

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- ROADMAP -->
## Roadmap

- [ ] some feature

See the [open issues](https://github.com/Novanglus96/{{PROJECT_NAME}}/issues) for a full list of proposed features (and known issues).

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**. Please follow these steps and guidelines to help us maintain a smooth development process.

### 1. Fork the Repository

- Click the **Fork** button at the top-right of this repository to create your own copy.
- Clone your fork locally.

### 2. Branch Naming
Create branches following this pattern:

- **Features**: feature/**branch-name** - *For new features or enhancements*.
- **Fixes**: fix/**branch-name** - *For bug fixes or patches*.

### 3. Pull Request Targets
Submit pull requests to the appropriate branch based on the stability of your changes:

| Target Branch | Purpose                                      |
| ------------- | -------------------------------------------- |
| main          | Production-ready changes for release.        |
| rc            | Release candidates for staging releases.     |
| alpha         | Experimental and unstable changes.           |
| beta          | More stable than alpha, for broader testing. |

*PRs to main and rc branches are for finalized changes intended for the next release.
PRs to alpha and beta are for testing and experimental work.*

### 4. Commit Message Format
We use semantic commit messages to automate changelog and versioning.

Format:

```cpp
<type>(optional scope): <short description>
```
| Common types |                                                         |
| ------------ | ------------------------------------------------------- |
| feat:        | A new feature                                           |
| fix:         | A bug fix                                               |
| chore:       | Changes to build process or auxiliary tools             |
| docs:        | Documentation only                                      |
| style:       | Formatting, missing semicolons, etc; no code change     |
| refactor:    | Code change that neither fixes a bug nor adds a feature |
| perf:        | Performance improvements                                |
| test:        | Adding or fixing tests                                  |

**Breaking changes**: Add ! after type or scope

```makefile
feat!: drop support for Node 10
fix(api)!: change endpoint response format
```

Examples:

- feat: add user profile page
- fix(auth): handle expired tokens gracefully
- chore: update dependencies
- perf: optimize image loading

### 5. Pull Request Checklist
Before submitting your PR, please ensure:

- Your branch is up to date with the target branch.
- Your code passes all tests and linters.
- You have added or updated tests if applicable.
- Relevant documentation has been added or updated.
- Your PR description clearly explains your changes and references related issues.

### 6. Testing Changes
Please test your changes locally or in a staging environment before opening a PR. Use alpha or beta branches for testing experimental changes.

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE.txt` for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Support

<a href="https://www.buymeacoffee.com/5Zn8Xh3l9" target="_blank"><img src="https://www.buymeacoffee.com/assets/img/custom_images/purple_img.png" alt="Buy Me A Coffee" style="height: 41px !important;width: 174px !important;box-shadow: 0px 3px 2px 0px rgba(190, 190, 190, 0.5) !important;-webkit-box-shadow: 0px 3px 2px 0px rgba(190, 190, 190, 0.5) !important;" ></a>

<p>Or</p> 

<a href="https://www.patreon.com/amitmerchant">
	<img src="https://c5.patreon.com/external/logo/become_a_patron_button@2x.png" width="160">
</a>

<!-- CONTACT -->
## Contact

John Adams - Lenore.Apps@gmail.com

Project Link: [https://github.com/Novanglus96/{{PROJECT_NAME}}](https://github.com/Novanglus96/{{PROJECT_NAME}})

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- ACKNOWLEDGMENTS -->
## Acknowledgements

A heartfelt thanks to our Patrons for their generous support! Your contributions help us maintain and improve this project.

### ⭐ Thank You to Our Supporters:

![Red Supporter Badge](https://img.shields.io/badge/Eleanor-E41B17?style=for-the-badge&logo=patreon&logoColor=gray)
![Red Supporter Badge](https://img.shields.io/badge/Danielle-E41B17?style=for-the-badge&logo=patreon&logoColor=gray)
![BuyMeACoffee Supporter Badge](https://img.shields.io/badge/SuperDev-white?style=for-the-badge&logo=buymeacoffee&logoColor=black)
<!--![Gold Supporter Badge](https://img.shields.io/badge/Eleanor-gold?style=for-the-badge&logo=patreon&logoColor=gray)-->
<!--![Silver Supporter Badge](https://img.shields.io/badge/Jane_Smith-silver?style=for-the-badge&logo=patreon&logoColor=gray)-->
<!--![BuyMeACoffee Supporter Badge](https://img.shields.io/badge/Jane_Smith-white?style=for-the-badge&logo=buymeacoffee&logoColor=black)-->

Want to see your name here? Support us on [Patreon](https://www.patreon.com/novanglus) to join our amazing community and shape the future of {{PROJECT_NAME}}!

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/Novanglus96/{{PROJECT_NAME}}?style=for-the-badge
[contributors-url]: https://github.com/Novanglus96/{{PROJECT_NAME}}/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/Novanglus96/{{PROJECT_NAME}}?style=for-the-badge
[forks-url]: https://github.com/Novanglus96/{{PROJECT_NAME}}/forks
[stars-shield]: https://img.shields.io/github/stars/Novanglus96/{{PROJECT_NAME}}?style=for-the-badge
[stars-url]: https://github.com/Novanglus96/{{PROJECT_NAME}}/stargazers
[issues-shield]: https://img.shields.io/github/issues/Novanglus96/{{PROJECT_NAME}}?style=for-the-badge
[issues-url]: https://github.com/Novanglus96/{{PROJECT_NAME}}/issues
[license-shield]: https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge
[license-url]: https://github.com/Novanglus96/{{PROJECT_NAME}}/blob/main/LICENSE
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://www.linkedin.com/in/johnmadamsjr
[product-screenshot]: images/screenshot.png
[Next.js]: https://img.shields.io/badge/next.js-000000?style=for-the-badge&logo=nextdotjs&logoColor=white
[Next-url]: https://nextjs.org/
[React.js]: https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB
[React-url]: https://reactjs.org/
[Vue.js]: https://img.shields.io/badge/Vue.js-35495E?style=for-the-badge&logo=vuedotjs&logoColor=4FC08D
[Vue-url]: https://vuejs.org/
[Angular.io]: https://img.shields.io/badge/Angular-DD0031?style=for-the-badge&logo=angular&logoColor=white
[Angular-url]: https://angular.io/
[Svelte.dev]: https://img.shields.io/badge/Svelte-4A4A55?style=for-the-badge&logo=svelte&logoColor=FF3E00
[Svelte-url]: https://svelte.dev/
[Laravel.com]: https://img.shields.io/badge/Laravel-FF2D20?style=for-the-badge&logo=laravel&logoColor=white
[Laravel-url]: https://laravel.com
[Bootstrap.com]: https://img.shields.io/badge/Bootstrap-563D7C?style=for-the-badge&logo=bootstrap&logoColor=white
[Bootstrap-url]: https://getbootstrap.com
[JQuery.com]: https://img.shields.io/badge/jQuery-0769AD?style=for-the-badge&logo=jquery&logoColor=white
[JQuery-url]: https://jquery.com 
[Django]: https://img.shields.io/badge/django-092E20?style=for-the-badge&logo=django&logoColor=white
[Django-url]: https://www.djangoproject.com/
[Docker]: https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white
[Docker-url]: https://www.docker.com/