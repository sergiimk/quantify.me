package me.quantify.sandbox;

import com.sun.jersey.api.container.filter.GZIPContentEncodingFilter;
import com.sun.jersey.api.container.grizzly2.GrizzlyServerFactory;
import com.sun.jersey.api.core.PackagesResourceConfig;
import com.sun.jersey.api.core.ResourceConfig;
import org.glassfish.grizzly.http.server.HttpServer;

import javax.ws.rs.core.UriBuilder;
import java.io.IOException;
import java.net.URI;
import java.util.logging.Logger;

public class Main {

	private static Logger logger = Logger.getLogger("me.quantify.sandbox");

	private static HttpServer startServer() throws IOException {
		logger.info("Starting server...");

		URI uri = UriBuilder
				.fromUri("http://0.0.0.0")
				.port(8080)
				.build();

		ResourceConfig cfg = new PackagesResourceConfig("me.quantify.sandbox");
		cfg.getContainerRequestFilters().add(new GZIPContentEncodingFilter());
		cfg.getContainerResponseFilters().add(new GZIPContentEncodingFilter());

		return GrizzlyServerFactory.createHttpServer(uri, cfg);
	}

	public static void main(String[] args) throws IOException {
		HttpServer server = startServer();

		logger.info("Server started, hit enter to stop.");
		System.in.read();

		server.stop();
	}
}
