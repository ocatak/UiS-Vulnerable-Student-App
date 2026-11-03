workspace {

    model {

        customer = person "Customer"

        juiceShop = softwareSystem "OWASP Juice Shop" {

            webapp = container "Angular SPA" "Browser-based frontend" "JavaScript/Angular"

            backend = container "Node.js Backend" "Business logic and APIs" "Node.js + Express"

            database = container "Database" "Stores users, products and orders" "SQLite"
        }

        customer -> webapp "Uses"

        webapp -> backend "REST/JSON"
        backend -> database "Reads/Writes"
    }

    views {
        container juiceShop {
            include *
            autolayout lr
        }
    }
}
