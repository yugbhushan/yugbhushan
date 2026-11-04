import com.comsol.model.Model;
import com.comsol.model.util.ModelUtil;

/**
 * Portfolio reconstruction. SI units throughout. Build and solve two annular
 * half-rotor scenarios under an azimuthally averaged braking pulse.
 */
public class DiscBrakeStudy {
    public static Model build(String tag, String label, double rho, double cp, double k) {
        Model model = ModelUtil.create(tag);
        model.label(label);
        model.param().set("Ri", "0.055[m]");
        model.param().set("Ro", "0.145[m]");
        model.param().set("H", "0.010[m]");
        model.param().set("Tamb", "293.15[K]");
        model.param().set("qpeak", "600000[W/m^2]");
        model.param().set("tstop", "4[s]");
        model.param().set("hfilm", "35[W/(m^2*K)]");
        model.param().set("emis", "0.8");
        model.param().set("sigmaSB", "5.670374419e-8[W/(m^2*K^4)]");

        model.component().create("rotor", true);
        var part = model.component("rotor");
        part.geom().create("g", 3);
        var geometry = part.geom("g");
        geometry.create("outer", "Cylinder");
        geometry.feature("outer").set("r", "Ro");
        geometry.feature("outer").set("h", "H");
        geometry.create("bore", "Cylinder");
        geometry.feature("bore").set("r", "Ri");
        geometry.feature("bore").set("h", "H");
        geometry.create("annulus", "Difference");
        geometry.feature("annulus").selection("input").set("outer");
        geometry.feature("annulus").selection("input2").set("bore");
        geometry.run();

        part.selection().create("rubbingFace", "Box");
        var face = part.selection("rubbingFace");
        face.set("entitydim", 2);
        face.set("condition", "inside");
        face.set("zmin", "H-1e-7[m]");
        face.set("zmax", "H+1e-7[m]");
        if (face.entities(2).length != 1) {
            throw new IllegalStateException("Expected exactly one annular rubbing face.");
        }

        part.material().create("solid", "Common");
        part.material("solid").label(label);
        var properties = part.material("solid").propertyGroup("def");
        properties.set("density", rho + "[kg/m^3]");
        properties.set("heatcapacity", cp + "[J/(kg*K)]");
        properties.set("thermalconductivity", k + "[W/(m*K)]");

        part.physics().create("ht", "HeatTransferInSolids", "g");
        var heat = part.physics("ht");
        heat.feature("init1").set("Tinit", "Tamb");
        heat.create("rubbing", "HeatFluxBoundary", 2);
        heat.feature("rubbing").selection().named("rubbingFace");
        // Positive q0 is inward. The bottom and cylindrical edges are insulated.
        heat.feature("rubbing").set("q0",
            "qpeak*max(0,1-t/tstop)*2*sqrt(x^2+y^2)/(Ri+Ro)"
            + "-hfilm*(T-Tamb)-emis*sigmaSB*(T^4-Tamb^4)");

        part.mesh().create("mesh1");
        part.mesh("mesh1").autoMeshSize(3);
        part.mesh("mesh1").run();
        model.study().create("braking");
        model.study("braking").create("time", "Transient");
        model.study("braking").feature("time").set("tlist", "range(0,0.1,30)");
        model.study("braking").run();
        return model;
    }

    public static void main(String[] args) throws java.io.IOException {
        Model iron = build("Iron", "Gray cast iron", 7200, 500, 52);
        iron.save("disc-brake-iron.mph");
        ModelUtil.remove("Iron");
        Model ceramic = build("Ceramic", "Illustrative SiC composite", 2500, 800, 35);
        ceramic.save("disc-brake-sic.mph");
    }
}
