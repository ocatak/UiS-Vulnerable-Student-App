workspace "OWASP Juice Shop" {

    model {
        customer = person "Customer" "Browses products and places orders"{
            tags "Human"
        }
        shopkeeper = person "Shopkeeper" "Manages the shop adding, removing wares and changing prices."{
            tags "Human"
        }
        admin = person "Administrator" "Manages the application"{
            tags "Human"
        }
        
        juiceShop = softwareSystem "OWASP Juice Shop" "Intentionally vulnerable web application"{
            tags "shop"
            webapp = container "Frontend" "Frontend application" "Angular"{
                angular = component "Angular SPA" {
                    tags "PID"
                }
                material = component "Material"
            }

            api = container "REST API" "Business logic and endpoints" "Node.js/Express"{
                express = component "Express"{
                    tags "PID"
                }
                noSqlDatabase = component "NoSql Database"
                sequelize = component "Sequelizer"
                express -> noSqlDatabase
                express -> sequelize
            }

            database = container "Database" "Stores users, products and orders" "SQLite"{
                fileStorage = component "File storage"
                sQLite = component "SQLite"{
                    tags "PID"
                }
            }

            sequelize -> sQLite "SQL"
            sequelize -> sQLite "Dynamic API"

            
            angular -> express "Service API"
            angular -> express "socket IO"
            express -> angular "socket IO"

            

            webapp -> api "Makes API calls"
            api -> database "Reads and writes data"
        }


        customer -> juiceShop "Uses"
        shopkeeper -> juiceShop "Shopkeep"
        admin -> juiceShop "Administers"
    }

    views {
        systemContext juiceShop {
            include *
            autolayout lr
        }
    
        container juiceShop {
            include *
            autolayout lr
        }
        
        component webapp {
            include *
            autolayout lr
        }
        
        component api {
            include *
            autolayout lr
        }

        component database {
            include *
            autolayout lr
        }
    }
}