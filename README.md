# CTFD-Status-Page
[CTFd](https://ctfd.io) plugin to display a status page for event participants, showing the ranking (TOP X) in a random order, the support workload, CTFd statistics, and more.

<p align="center">
  <img src="https://github.com/user-attachments/assets/a02a8ac6-ca34-4d9d-a808-ea7be0bf2c41" alt="2025-07-07 13_55_26-Finale HACKOSINT 2025 — Mozilla Firefox" width="600" style="border-radius: 12px;">
</p>

---

## Main features

This plugin displays various blocks: 
- **Randomized scoreboard**: Displays the TOP X in a random order, allowing teams to see if they are among the top without knowing their exact position.
- **Live statistics**: Shows the number of submissions (correct and incorrect) made during the event on the platform.
- **Remaining time**: Displays the time left until the end of the event.
- **Support workload**: Shows the current support load, to inform participants if the support team is overwhelmed or available.

Each block can be enabled or disabled individually from the plugin administration panel, allowing for fully customizable display.

## Why this plugin?

During the HACK'OSINT CTF 2025, we created a "status" page allowing participants to follow the event live, check the ranking, and more (more information : [Status-Page-HACKOSINTCTF2025](https://www.linkedin.com/feed/update/urn:li:activity:7313440206802608129)).
We then wanted to make this system accessible to everyone by creating a public CTFd plugin.  
This allows, for example, a team to know if they are in the TOP X even if the global scoreboard is hidden.

## Installation

1. Clone this repository into your `CTFd/plugins` folder:

   ```bash
   cd /path/to/CTFd/plugins
   git clone https://github.com/HACK-OLYTE/CTFD-Status-Page.git

2. Restart your CTFd instance to load the plugin.

## Configuration

Go to the **Plugins > Status-page** section in the admin panel to:

- Enable or disable the display of each block.
- Set an event end date, configure the TOP X value to display, define the support load, etc.

Here is a demo video of the plugin:
https://github.com/user-attachments/assets/bef632d4-6ec1-4cf4-9726-3c1dc34eedc1

## Dependencies

- CTFd ≥ v3.x
- Compatible with both Docker and local installations.
- A modern browser with JavaScript enabled.

## Support

For any questions or issues, open an [issue](https://github.com/votre-utilisateur/CTFD-Attempts-Remover/issues).  
Or contact us via the Hack'olyte association website: [contact](https://hackolyte.fr/contact/).

## Contributing

Contributions are welcome!  
You can:

- Report bugs
- Suggest new features
- Submit pull requests

## License

This plugin is licensed under [CC BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/deed.en).  
Please do not remove the footer from each HTML file without prior permission from the Hack'olyte association.

