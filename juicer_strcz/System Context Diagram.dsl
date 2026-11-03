workspace "OWASP Juice Shop" {

    model {
        customer = person "Customer" "Browses products and places orders"
        admin = person "Administrator" "Manages the application"

        juiceShop = softwareSystem "OWASP Juice Shop" "Intentionally vulnerable web application"

        customer -> juiceShop "Uses"
        admin -> juiceShop "Administers"
    }

    views {
        systemContext juiceShop {
            include *
            autolayout lr
        }

        theme default
    }
}
