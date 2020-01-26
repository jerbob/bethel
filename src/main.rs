use actix_files::{Files, NamedFile};
use actix_web::{web, App, HttpServer, Result}; 


async fn index() -> Result<NamedFile> {
    Ok(NamedFile::open("static/index.html")?)
}


async fn presentation() -> Result<NamedFile> {
    Ok(NamedFile::open("static/presentation.html")?)
}


#[actix_rt::main]
async fn main() -> std::io::Result<()> {
    println!("Serving on localhost port 8000...");
    HttpServer::new(move || {
        App::new()
            .service(Files::new("/static/", "static/"))
            .service(web::resource("/").route(web::get().to(index)))
            .service(web::resource("/presentation").route(web::get().to(presentation)))
    })
    .bind("127.0.0.1:8000")?
    .run()
    .await
}

