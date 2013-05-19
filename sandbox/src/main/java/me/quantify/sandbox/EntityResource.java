package me.quantify.sandbox;

import com.sun.jersey.api.core.ResourceContext;

import javax.ws.rs.*;
import javax.ws.rs.core.Context;

@Path("/entities")
public class EntityResource {

	@Path("{id}/events")
	public EventResource eventResource(
			@Context ResourceContext rc,
			@PathParam("id") long entityId) {
		EventResource evnt = rc.getResource(EventResource.class);
		evnt.entityId = entityId;
		return evnt;
	}

	@GET
	@Path("{id}")
	@Produces("text/plain")
	public String getEntityInfo(@PathParam("id") long entityId) {
		return String.format("YOLO from entity %s", entityId);
	}

}
