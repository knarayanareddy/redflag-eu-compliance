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

// This is an unverified allegation copied from the demo request, not an ingested or verified EU alert.
export const UNVERIFIED_ALERT_REFERENCE = {
  alertNumber: 'A12/00123/24',
  riskDescription: 'The demo request describes magnetic pinch and bowel perforation risk.',
  sourceStatus: 'UNVERIFIED — no official Safety Gate record, citation, or source URL is bundled.',
};
