package me.quantify.sandbox;

import javax.ws.rs.*;
import javax.ws.rs.core.*;
import java.net.URI;

public class EventResource {

	public long entityId;

	@Context
	public UriInfo uriInfo;

	@GET
	@Path("{id}")
	@Produces("text/plain")
	public String getEvent(@PathParam("id") long eventId) {
		return String.format("entity %s event %s here!", entityId, eventId);
	}

	@POST
	@Consumes("text/plain")
	public Response createEvent(String data) {
		UriBuilder ub = uriInfo.getAbsolutePathBuilder();
		URI uri = ub.path(Integer.toString(1234)).build();
		return Response.created(uri).build();
	}

}
