workspace "OWASP Juice Shop Security" {

    model {

        attacker = person "Attacker" "Attempts to exploit vulnerabilities"

        customer = person "Customer"

        juiceShop = softwareSystem "OWASP Juice Shop" {

            webapp = container "Angular SPA" "Frontend application" "Angular"

            api = container "Node.js API" "Business logic and REST endpoints" "Node.js/Express"

            database = container "Database" "Stores users, products and orders" "SQLite"
        }

        customer -> webapp "Uses"

        attacker -> webapp "Attempts XSS attacks"

        attacker -> api "Attempts injection and access control attacks"

        webapp -> api "REST/JSON"

        api -> database "Reads/Writes"
    }

    views {

        container juiceShop {
            include *
            autolayout lr
        }

    }
}