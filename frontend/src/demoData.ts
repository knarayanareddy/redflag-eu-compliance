export type DemoProduct = {
  id: string;
  title: string;
  category: string;
  demoAttributes: string[];
  note: string;
};

// The task supplied these product titles; they are example inputs, not live marketplace records.
export const DEMO_PRODUCTS: DemoProduct[] = [
  {
    id: 'magnetic-spheres',
    title: 'Magnetic Building Spheres 216pcs',
    category: 'Toy · magnet-topic demo focus (not a risk rating)',
    demoAttributes: ['magnetic', 'building spheres', '216pcs'],
    note: 'Synthetic title-only marketplace example; no manufacturer, GTIN, or seller documents supplied.',
  },
  {
    id: 'gan-charger',
    title: '65W USB-C GaN Fast Wall Charger',
    category: 'Electrical · charger-safety demo focus',
    demoAttributes: ['65W', 'USB-C', 'GaN', 'wall charger'],
    note: 'Synthetic title-only marketplace example; no model, manufacturer, or test documents supplied.',
  },
  {
    id: 'herbal-cream',
    title: 'Gentle Herbal Facial Cream',
    category: 'Cosmetics · product-information demo focus',
    demoAttributes: ['herbal', 'facial cream'],
    note: 'Synthetic title-only marketplace example; no ingredient list, responsible person, or packaging supplied.',
  },
];

/**
 * Synthetic scenario fixture whose fields and UI behavior were checked for this demo.
 * Its alert-shaped reference and hazard narrative came from the mission prompt only;
 * it is not an authenticated EU Safety Gate record and must never be cited as one.
 */
export const VERIFIED_DEMO_RECALL_FIXTURE = {
  fixtureId: 'synthetic-demo-A12-00123-24',
  displayReference: 'A12/00123/24',
  synthetic: true,
  verifiedForDemonstration: true,
  officialSafetyGateRecordVerified: false,
  productFamily: 'Magnetic sphere toy scenario',
  riskDescription: 'Mission-supplied scenario: magnetic pinch and bowel perforation hazard.',
  matchTerms: ['magnetic'],
  sourceStatus: 'Verified as a synthetic demo fixture only; not verified against an official EU record.',
};
